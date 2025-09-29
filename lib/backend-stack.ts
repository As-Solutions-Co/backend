import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as apigtw from "aws-cdk-lib/aws-apigateway";

import * as ec2 from "aws-cdk-lib/aws-ec2";
import * as iam from "aws-cdk-lib/aws-iam";
import * as rds from "aws-cdk-lib/aws-rds";
import * as sm from "aws-cdk-lib/aws-secretsmanager";
import * as kms from "aws-cdk-lib/aws-kms";
import * as triggers from "aws-cdk-lib/triggers";
import * as path from "path";
import * as fs from "fs-extra";
import * as os from "os";
import { exec } from "child_process";
import { PythonLayerVersion } from "@aws-cdk/aws-lambda-python-alpha";

export class BackendStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const project_runtime = lambda.Runtime.PYTHON_3_13;
    const project_vpc = ec2.Vpc.fromLookup(this, "test", {
      vpcId: "vpc-0562917520fe32449",
    });

    const default_vpc_sg = ec2.SecurityGroup.fromLookupById(
      this,
      "default_sg",
      "sg-0665ce570fe1b5d46"
    );

    const srcPath = path.join(__dirname, "..", "src");
    const tempDeps = path.join(os.tmpdir(), "temp-deps");
    const depFiles = ["pyproject.toml", "uv.lock"];
    fs.ensureDirSync(tempDeps);

    depFiles.forEach((file) => {
      const filePath = path.join(srcPath, file);
      if (fs.existsSync(filePath)) {
        fs.copySync(filePath, path.join(tempDeps, file));
      }
    });

    const dependenciesLayer = new PythonLayerVersion(this, "Dependenci_layer", {
      entry: tempDeps,
      compatibleArchitectures: [lambda.Architecture.ARM_64],
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_13],
    });

    const powerToolsLayer = lambda.LayerVersion.fromLayerVersionArn(
      this,
      "Powertools layer",
      "arn:aws:lambda:us-east-1:017000801446:layer:AWSLambdaPowertoolsPythonV3-python313-arm64:19"
    );

    const shared_code_layer = new lambda.LayerVersion(
      this,
      "shared_code_layer",
      {
        compatibleRuntimes: [project_runtime],
        description: "Includes generic code like db connection",
        code: lambda.Code.fromAsset("./src/shared"),
      }
    );

    const project_db = new rds.DatabaseCluster(this, "academy_db", {
      engine: rds.DatabaseClusterEngine.auroraPostgres({
        version: rds.AuroraPostgresEngineVersion.VER_17_4,
      }),
      writer: rds.ClusterInstance.serverlessV2("writer_instance", {
        publiclyAccessible: false,
      }),
      readers: [
        rds.ClusterInstance.serverlessV2("reader", { scaleWithWriter: true }),
      ],
      serverlessV2MinCapacity: 0,
      serverlessV2AutoPauseDuration: cdk.Duration.minutes(5),
      serverlessV2MaxCapacity: 15,
      credentials: rds.Credentials.fromGeneratedSecret("postgres"),
      vpc: project_vpc,
      vpcSubnets: project_vpc.selectSubnets({
        subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
      }),
      enableDataApi: true,
      securityGroups: [default_vpc_sg],
    });

    const secret_arn = project_db.secret?.secretArn;

    if (!secret_arn) return;

    const database_secret = sm.Secret.fromSecretCompleteArn(
      this,
      "database_secret",
      secret_arn
    );

    const layer_dir = path.join(os.tmpdir(), "models_layer");
    const src = path.join(__dirname, "..", "src", "resources");
    const dest = path.join(layer_dir, "python");
    fs.ensureDirSync(src);
    fs.ensureDirSync(dest);
    fs.copySync(src, dest);

    const models_layer = new lambda.LayerVersion(this, "models_layer", {
      code: lambda.Code.fromAsset(layer_dir, {
        exclude: ["**/crud.py", "**/main.py"],
        ignoreMode: cdk.IgnoreMode.GIT,
      }),
      compatibleRuntimes: [project_runtime],
      description: "Capa con módulos models.py",
    });

    const db_schema_fn = new lambda.Function(this, "db_schema_function", {
      runtime: project_runtime,
      handler: "db_init.handler",
      code: lambda.Code.fromAsset(path.join(__dirname, "..", "src"), {
        exclude: ["**", "!db_init.py"],
        ignoreMode: cdk.IgnoreMode.GIT,
      }),
      securityGroups: [default_vpc_sg],
      timeout: cdk.Duration.minutes(5),
      layers: [dependenciesLayer, shared_code_layer, models_layer],
      vpc: project_vpc,
      vpcSubnets: project_vpc.selectSubnets({
        subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
      }),
      environment: {
        SECRET_ARN: database_secret.secretArn,
        DB_NAME: "postgres",
      },
      architecture: lambda.Architecture.ARM_64,
    });

    const organization_manager = new lambda.Function(
      this,
      "Organization manager",
      {
        runtime: project_runtime,
        code: lambda.Code.fromAsset("./src/resources/organizations/"),
        handler: "main.handler",
        layers: [dependenciesLayer, shared_code_layer, powerToolsLayer],
        vpc: project_vpc,
        vpcSubnets: project_vpc.selectSubnets({
          subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
        }),
        environment: {
          SECRET_ARN: database_secret.secretArn,
          DB_NAME: "postgres",
        },
        securityGroups: [default_vpc_sg],
        timeout: cdk.Duration.seconds(20),
        architecture: lambda.Architecture.ARM_64,
        memorySize: 256,
      }
    );

    const api = new apigtw.RestApi(this, "academy_api");

    const organization_resource = api.root.addResource("organizations");

    organization_resource.addMethod(
      "GET",
      new apigtw.LambdaIntegration(organization_manager)
    );

    organization_resource.addMethod(
      "POST",
      new apigtw.LambdaIntegration(organization_manager)
    );

    organization_resource
      .addResource("swagger")
      .addMethod("GET", new apigtw.LambdaIntegration(organization_manager));

    const organization_id_resource = organization_resource.addResource("{id}");

    organization_id_resource.addMethod(
      "GET",
      new apigtw.LambdaIntegration(organization_manager)
    );
    organization_id_resource.addMethod(
      "DELETE",
      new apigtw.LambdaIntegration(organization_manager)
    );

    project_db.grantConnect(organization_manager, "postgres");
    database_secret.grantRead(organization_manager);
    database_secret.grantRead(db_schema_fn);
  }
}

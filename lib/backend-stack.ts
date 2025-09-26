import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as apigtw from "aws-cdk-lib/aws-apigatewayv2";
import * as integrations from "aws-cdk-lib/aws-apigatewayv2-integrations";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import * as iam from "aws-cdk-lib/aws-iam";
import * as rds from "aws-cdk-lib/aws-rds";
import * as sm from "aws-cdk-lib/aws-secretsmanager";
import * as kms from "aws-cdk-lib/aws-kms";
import * as triggers from "aws-cdk-lib/triggers";
import * as path from "path";
import * as fs from "fs-extra";
import * as os from "os";

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

    const requirements_layer = new lambda.LayerVersion(
      this,
      "dependencies_layer",
      {
        compatibleRuntimes: [project_runtime],
        description: "Includes all project requirements",
        code: lambda.Code.fromAsset("./src/dependencies/"),
      }
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
      layers: [requirements_layer, shared_code_layer, models_layer],
      vpc: project_vpc,
      vpcSubnets: project_vpc.selectSubnets({
        subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
      }),
      environment: {
        SECRET_ARN: database_secret.secretArn,
        DB_NAME: "postgres",
      },
    });

    // const db_schema_trigger = new triggers.Trigger(this, "db_schema_trigger", {
    //   handler: db_schema_fn,
    //   timeout: cdk.Duration.minutes(10),
    //   invocationType: triggers.InvocationType.EVENT,
    //   executeAfter: [project_db, db_schema_fn],
    // });

    const organization_manager = new lambda.Function(
      this,
      "Organization manager",
      {
        runtime: project_runtime,
        code: lambda.Code.fromAsset("./src/resources/organizations/"),
        handler: "main.handler",
        layers: [requirements_layer, shared_code_layer],
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
      }
    );

    const api = new apigtw.HttpApi(this, "api");

    api.addRoutes({
      path: "/organization/{id}",
      methods: [apigtw.HttpMethod.GET],
      integration: new integrations.HttpLambdaIntegration(
        "get_organization_by_id",
        organization_manager
      ),
    });
    api.addRoutes({
      path: "/organization",
      methods: [apigtw.HttpMethod.GET],
      integration: new integrations.HttpLambdaIntegration(
        "get_organizations",
        organization_manager
      ),
    });

    api.addRoutes({
      path: "/organization",
      methods: [apigtw.HttpMethod.POST],
      integration: new integrations.HttpLambdaIntegration(
        "post_organization",
        organization_manager
      ),
    });

    project_db.grantConnect(organization_manager, "postgres");
    database_secret.grantRead(organization_manager);
    database_secret.grantRead(db_schema_fn);
  }
}

import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as apigtw from "aws-cdk-lib/aws-apigateway";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import * as iam from "aws-cdk-lib/aws-iam";
import * as rds from "aws-cdk-lib/aws-rds";

export class BackendStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const project_runtime = lambda.Runtime.PYTHON_3_13;
    const project_vpc = ec2.Vpc.fromLookup(this, "test", {
      vpcId: "vpc-0f728e80e72c63ceb",
    });

    const requirements_layer = new lambda.LayerVersion(
      this,
      "requirements_layer",
      {
        compatibleRuntimes: [project_runtime],
        description: "Includes all project requirements",
        code: lambda.Code.fromAsset("./src/requirements_layer/"),
      }
    );

    const organization_models_layer = new lambda.LayerVersion(
      this,
      "organization_models",
      {
        compatibleRuntimes: [project_runtime],
        code: lambda.Code.fromAsset("./src/resources/organizations/models"),
      }
    );

    const sg1 = ec2.SecurityGroup.fromLookupById(
      this,
      "existing sg1",
      "sg-0d56636fc8ecdbab8"
    );
    const sg2 = ec2.SecurityGroup.fromLookupById(
      this,
      "existing sg2",
      "sg-059c6c6a5482ef419"
    );

    const db_proxy = rds.DatabaseProxy.fromDatabaseProxyAttributes(
      this,
      "existing proxy",
      {
        dbProxyName: "proxy-1758654364540-academy",
        endpoint:
          "proxy-1758654364540-academy.proxy-c89aw02c2ls0.us-east-1.rds.amazonaws.com",
        securityGroups: [sg1, sg2],
        dbProxyArn:
          "arn:aws:rds:us-east-1:659788916661:db-proxy:prx-06e65d9c4bf7a4e97",
      }
    );

    const create_organization_fn = new lambda.Function(
      this,
      "create organization",
      {
        runtime: project_runtime,
        code: lambda.Code.fromAsset(
          "./src/resources/organizations/create_organization"
        ),
        handler: "main.handler",
        layers: [requirements_layer, organization_models_layer],
        vpc: project_vpc,
        allowPublicSubnet: true,
        timeout: cdk.Duration.seconds(10),
        environment: {
          SECRET_NAME: "rds!db-dca1ac4a-ca72-4ba3-8e38-fd233986ad88",
        },
      }
    );

    db_proxy.grantConnect(create_organization_fn, "postgres");
  }
}

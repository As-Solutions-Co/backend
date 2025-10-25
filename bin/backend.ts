#!/usr/bin/env node
import * as cdk from "aws-cdk-lib";
import { BackendStack } from "../lib/backend-stack";

const app = new cdk.App();
new BackendStack(app, "BackendStack", {
  env: { account: "057149785827", region: "us-east-1" },
});

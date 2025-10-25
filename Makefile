test:
	cdk synth
	sam local start-api -t cdk.out/BackendStack.template.json -n env.json --docker-network aws_network --warm-containers eager
import pulumi

config = pulumi.Config()

# Project configuration
PROJECT_NAME = config.get("projectName") or "lambda-webhook"
STACK = pulumi.get_stack()

# AWS configuration
AWS_REGION = config.get("awsRegion") or "ap-southeast-1"

# ECR configuration
ECR_REPO_NAME = f"{PROJECT_NAME}-repo"

# Lambda configuration
LAMBDA_NAME = f"{PROJECT_NAME}-function"
LAMBDA_TIMEOUT = 300
LAMBDA_MEMORY = 256

# API Gateway configuration
API_GATEWAY_NAME = f"{PROJECT_NAME}-api"
API_STAGE_NAME = "prod"
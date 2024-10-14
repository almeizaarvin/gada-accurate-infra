import pulumi
import pulumi_aws as aws
import base64
from pulumi import Config

# Load configuration
config = Config()

# AWS provider
aws_provider = aws.Provider("aws", region=config.require("awsRegion"))

# Create ECR repository
ecr_repo = aws.ecr.Repository("my-fastapi-repo",
    image_tag_mutability="MUTABLE",
    opts=pulumi.ResourceOptions(provider=aws_provider)
)

# Build Docker image
def get_registry_info(rid):
    creds = aws.ecr.get_credentials(registry_id=rid)
    decoded = creds.authorization_token.apply(lambda token: base64.b64decode(token).decode())
    return {
        "server": creds.proxy_endpoint,
        "username": decoded.split(':')[0],
        "password": decoded.split(':')[1]
    }

image = aws.ecr.get_repository(ecr_repo.name).repository_url.apply(lambda repo_url: aws.ecr.Image(
    f"{repo_url}:latest",
    image_name=repo_url,
    build=docker.DockerBuild(context=pulumi.Config().get("context") or "."),
    registry=get_registry_info(ecr_repo.registry_id)
))

# Create Lambda function
lambda_role = aws.iam.Role("my-fastapi-role",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Effect": "Allow"
            }
        ]
    }""",
    opts=pulumi.ResourceOptions(provider=aws_provider)
)

lambda_function = aws.lambda_.Function("my-fastapi-lambda",
    image_uri=image.image_name,
    package_type="Image",
    role=lambda_role.arn,
    memory_size=256,
    timeout=30,
    opts=pulumi.ResourceOptions(provider=aws_provider)
)

# Create API Gateway
api = aws.apigateway.RestApi("my-fastapi-api",
    opts=pulumi.ResourceOptions(provider=aws_provider)
)

resource = aws.apigateway.Resource("my-fastapi-resource",
    rest_api=api.id,
    parent_id=api.root_resource_id,
    path_part="{proxy+}",
    opts=pulumi.ResourceOptions(provider=aws_provider)
)

method = aws.apigateway.Method("my-fastapi-method",
    rest_api=api.id,
    resource_id=resource.id,
    http_method="ANY",
    authorization="NONE",
    opts=pulumi.ResourceOptions(provider=aws_provider)
)

integration = aws.apigateway.Integration("my-fastapi-integration",
    rest_api=api.id,
    resource_id=resource.id,
    http_method=method.http_method,
    integration_http_method="POST",
    type="AWS_PROXY",
    uri=lambda_function.invoke_arn,
    opts=pulumi.ResourceOptions(provider=aws_provider)
)

deployment = aws.apigateway.Deployment("my-fastapi-deployment",
    rest_api=api.id,
    stage_name="prod",
    opts=pulumi.ResourceOptions(depends_on=[method], provider=aws_provider)
)

pulumi.export("api_url", deployment.invoke_url)

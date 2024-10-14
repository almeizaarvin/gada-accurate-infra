import pulumi
import pulumi_aws as aws
from pulumi import FileAsset
from config import *  

aws_provider = aws.Provider("aws", region=AWS_REGION)

# Membuat role untuk Lambda
lambda_role = aws.iam.Role(f"{PROJECT_NAME}-lambda-role",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Effect": "Allow",
                "Sid": ""
            }
        ]
    }""",
    opts=pulumi.ResourceOptions(provider=aws_provider)
)

# Melampirkan kebijakan eksekusi dasar untuk Lambda
aws.iam.RolePolicyAttachment(f"{PROJECT_NAME}-lambda-policy-attachment",
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    role=lambda_role.name,
    opts=pulumi.ResourceOptions(provider=aws_provider)
)

# Membuat Lambda function
lambda_function = aws.lambda_.Function(LAMBDA_NAME,
    code=FileAsset("lambda_function.zip"),  # Menggunakan file zip yang telah dibuat
    handler="__main__.handler",  # Menggunakan handler dari __main__.py
    runtime="python3.8",  # Ganti dengan runtime yang sesuai
    role=lambda_role.arn,
    timeout=LAMBDA_TIMEOUT,
    memory_size=LAMBDA_MEMORY,
    opts=pulumi.ResourceOptions(provider=aws_provider)
)

# Membuat API Gateway
api = aws.apigateway.RestApi(API_GATEWAY_NAME,
    opts=pulumi.ResourceOptions(provider=aws_provider)
)

resource = aws.apigateway.Resource("anyResource",
    rest_api=api.id,
    parent_id=api.root_resource_id,
    path_part="{proxy+}",
    opts=pulumi.ResourceOptions(provider=aws_provider)
)

method = aws.apigateway.Method("anyMethod",
    rest_api=api.id,
    resource_id=resource.id,
    http_method="ANY",
    authorization="NONE",
    opts=pulumi.ResourceOptions(provider=aws_provider)
)

integration = aws.apigateway.Integration("lambdaIntegration",
    rest_api=api.id,
    resource_id=resource.id,
    http_method=method.http_method,
    integration_http_method="POST",
    type="AWS_PROXY",
    uri=lambda_function.invoke_arn,
    opts=pulumi.ResourceOptions(provider=aws_provider)
)

deployment = aws.apigateway.Deployment(f"{PROJECT_NAME}-deployment",
    rest_api=api.id,
    stage_name=API_STAGE_NAME,
    opts=pulumi.ResourceOptions(depends_on=[method], provider=aws_provider)
)

# Output URL API Gateway
pulumi.export("api_url", deployment.invoke_url)

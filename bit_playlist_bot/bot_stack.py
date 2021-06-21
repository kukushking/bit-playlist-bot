import subprocess
from aws_cdk import (
    aws_apigateway as _api,
    aws_dynamodb as _dynamodb,
    aws_iam as _iam,
    aws_lambda as _lambda,
    core as _core,
)


class BitPlaylistBotStack(_core.Stack):

    def __init__(self, scope: _core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        layer: _lambda.ILayerVersion = self.create_dependencies_layer("./requirements.txt", ".layer/")

        message_handler: _lambda.IFunction = _lambda.Function(
            self,
            "tg-message-handler",
            code=_lambda.Code.from_asset("bit_playlist_bot"),
            handler="lambda.handler.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            layers=[layer],
            timeout=_core.Duration.minutes(1),
            dead_letter_queue_enabled=True,
        )
        message_handler.add_to_role_policy(
            _iam.PolicyStatement(
                actions=["secretsmanager:GetSecretValue"],
                resources=["*"],
            )
        )
        message_handler.add_to_role_policy(
            _iam.PolicyStatement(
                actions=["ssm:GetParameter"],
                resources=["*"],
            )
        )
        message_handler.add_to_role_policy(
            _iam.PolicyStatement(
                actions=[
                    "dynamodb:GetItem",
                    "dynamodb:PutItem",
                ],
                resources=["*"],
            )
        )
        _api.LambdaRestApi(
            self,
            "api-gateway",
            handler=message_handler,
        )
        _dynamodb.Table(
            self,
            "token-cache",
            table_name="token_info",
            partition_key=_dynamodb.Attribute(
                name="name",
                type=_dynamodb.AttributeType.STRING,
            ),
        )

    def create_dependencies_layer(self, requirements_path: str, output_dir: str) -> _lambda.LayerVersion:
        subprocess.check_call(
            f"pip install -r {requirements_path} -t {output_dir}/python".split()
        )
        return _lambda.LayerVersion(
            self, "requirements", code=_lambda.Code.from_asset(output_dir)
        )


#!/usr/bin/env python3
""" CDK Configuration for the backend stack."""

from aws_cdk import App, Stack, Tags, aws_iam
from constructs import Construct

from config import app_settings
from database.infrastructure.construct import RdsConstruct
from domain.infrastructure.construct import DomainConstruct
from network.infrastructure.construct import VpcConstruct
from raster_api.infrastructure.construct import RasterApiLambdaConstruct
from stac_api.infrastructure.construct import StacApiLambdaConstruct

app = App()


class DeployStack(Stack):
    """CDK stack for the backend stack."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """."""
        super().__init__(scope, construct_id, **kwargs)

        if app_settings.permissions_boundary_policy_name:
            permission_boundary_policy = aws_iam.Policy.from_policy_name(
                self,
                "permission-boundary",
                app_settings.permissions_boundary_policy_name,
            )
            aws_iam.PermissionsBoundary.of(self).apply(permission_boundary_policy)


deploy_stack = DeployStack(
    app,
    f"{app_settings.app_name}-{app_settings.stage_name()}",
    env=app_settings.cdk_env(),
)

if app_settings.vpc_id:
    vpc = VpcConstruct(
        deploy_stack,
        "network",
        vpc_id=app_settings.vpc_id,
        stage=app_settings.stage_name(),
    )
else:
    vpc = VpcConstruct(deploy_stack, "network", stage=app_settings.stage_name())

database = RdsConstruct(
    deploy_stack, "database", vpc.vpc, stage=app_settings.stage_name()
)

domain = DomainConstruct(deploy_stack, "domain", stage=app_settings.stage_name())

raster_api = RasterApiLambdaConstruct(
    deploy_stack,
    "raster-api",
    vpc=vpc.vpc,
    database=database,
    domain_name=domain.raster_domain_name,
)

stac_api = StacApiLambdaConstruct(
    deploy_stack,
    "stac-api",
    vpc=vpc.vpc,
    database=database,
    raster_api=raster_api,
    domain_name=domain.stac_domain_name,
)

# TODO this conditional supports deploying a second set of APIs to a separate custom domain and should be removed if no longer necessary
if app_settings.alt_domain():
    alt_domain = DomainConstruct(
        deploy_stack,
        "alt-domain",
        stage=app_settings.stage_name(),
        alt_domain=True,
    )

    alt_raster_api = RasterApiLambdaConstruct(
        deploy_stack,
        "alt-raster-api",
        vpc=vpc.vpc,
        database=database,
        domain_name=alt_domain.raster_domain_name,
    )

    alt_stac_api = StacApiLambdaConstruct(
        deploy_stack,
        "alt-stac-api",
        vpc=vpc.vpc,
        database=database,
        raster_api=raster_api,
        domain_name=alt_domain.stac_domain_name,
    )

for key, value in {
    "Project": app_settings.app_name,
    "Stack": app_settings.stage_name(),
    "Client": "nasa-impact",
    "Owner": "ds",
}.items():
    if value:
        Tags.of(app).add(key=key, value=value)

app.synth()

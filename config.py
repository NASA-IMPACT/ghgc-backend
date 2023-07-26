"""App settings."""
from typing import Optional

from pydantic import BaseSettings, Field


class vedaBackendAppSettings(BaseSettings):
    """Application settings."""

    # App name and deployment stage
    app_name: Optional[str] = Field(
        "backend",
        description="Optional app name used to name stack and resources",
    )
    project_prefix: Optional[str] = Field(
        None,
        description="Project prefix (ghgc/veda/...)",
    )
    stage: str = Field(
        ...,
        description=(
            "Deployment stage used to name stack and resources, "
            "i.e. `dev`, `staging`, `prod`"
        ),
    )
    vpc_id: Optional[str] = Field(
        None,
        description=(
            "Resource identifier of VPC, if none a new VPC with public and private "
            "subnets will be provisioned."
        ),
    )
    cdk_qualifier: Optional[str] = Field(
        "hnb659fds",
        description="CDK qualifier for deployment.",
    )
    aws_account_id: Optional[str] = Field(
        None,
        description="When deploying from a local machine the AWS account id is required to deploy to an exiting VPC",
    )
    aws_region: Optional[str] = Field(
        None,
        description="When deploying from a local machine the AWS region id is required to deploy to an exiting VPC",
    )
    permissions_boundary_policy_name: Optional[str] = Field(
        None,
        description="Name of IAM policy to define stack permissions boundary",
    )
    veda_domain_alt_hosted_zone_id: Optional[str] = Field(
        None,
        description="Route53 zone identifier if using a custom domain name",
    )
    veda_domain_alt_hosted_zone_name: Optional[str] = Field(
        None,
        description="Custom domain name, i.e. veda-backend.xyz",
    )

    def cdk_env(self) -> dict:
        """Load a cdk environment dict for stack"""

        if self.vpc_id:
            return {
                "account": self.aws_account_id,
                "region": self.aws_region,
            }
        else:
            return {}

    def alt_domain(self) -> bool:
        """True if alternative domain and host parameters provided"""
        return all(
            [
                self.veda_domain_alt_hosted_zone_id,
                self.veda_domain_alt_hosted_zone_name,
            ]
        )

    def stage_name(self) -> str:
        """Force lowercase stage name"""
        return self.stage.lower()

    class Config:
        """model config."""

        env_file = ".env"


backend_app_settings = vedaBackendAppSettings()

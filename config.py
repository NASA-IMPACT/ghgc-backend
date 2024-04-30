"""App settings."""
from typing import Optional

from pydantic import BaseSettings, Field


class vedaAppSettings(BaseSettings):
    """Application settings."""

    # App name and deployment stage
    app_name: Optional[str] = Field(
        "ghgc-backend",
        description="Optional app name used to name stack and resources",
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
    cdk_default_account: Optional[str] = Field(
        None,
        description="When deploying from a local machine the AWS account id is required to deploy to an exiting VPC",
    )
    cdk_default_region: Optional[str] = Field(
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
                "account": self.cdk_default_account,
                "region": self.cdk_default_region,
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

    def get_stac_catalog_url(self) -> Optional[str]:
        """Infer stac catalog url based on whether the app is configured to deploy the catalog to a custom subdomain or to a cloudfront route"""
        if self.veda_custom_host and self.veda_stac_root_path:
            return f"https://{veda_app_settings.veda_custom_host}{veda_app_settings.veda_stac_root_path}"
        if (
            self.veda_domain_create_custom_subdomains
            and self.veda_domain_hosted_zone_name
        ):
            return (
                f"https://{self.stage.lower()}-stac.{self.veda_domain_hosted_zone_name}"
            )
        return None

    class Config:
        """model config."""

        env_file = ".env"


veda_app_settings = vedaAppSettings()

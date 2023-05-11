"""Configuration options for a cloudfront distribution integration."""

from typing import Optional

from pydantic import BaseSettings, Field


class vedaCloudfrontSettings(BaseSettings):
    """Application settings"""

    cf_distribution_arn: Optional[str] = Field(
        None, description="Cloudfront distribution ARN"
    )
    raster_path_prefix: Optional[str] = Field(
        None,
        description=("Cloudfront behavior path pattern prefix for titiler api"),
    )
    stac_path_prefix: Optional[str] = Field(
        None,
        description=("Cloudfront behavior path pattern prefix for stac api"),
    )

    class Config:
        """model config"""

        env_file = ".env"
        env_prefix = "VEDA_"


veda_cloudfront_settings = vedaCloudfrontSettings()

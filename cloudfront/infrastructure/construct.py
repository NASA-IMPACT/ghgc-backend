"""CDK Construct for a custom API domain."""
from aws_cdk import Stack
from cdk_cloudfront_update.constructs import CloudfrontUpdate
from constructs import Construct

from .config import veda_cloudfront_settings


class CfConstruct(Construct):
    """CDK Construct for updating the cloudfront distribution."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        raster_api_url: str,
        stac_api_url: str,
        **kwargs,
    ) -> None:
        """."""
        super().__init__(scope, construct_id, **kwargs)

        stack_name = Stack.of(self).stack_name

        # STAC API
        stac_cf = CloudfrontUpdate(
            self,
            "stac-api-cf-update",
            distribution_arn=veda_cloudfront_settings.cf_distribution_arn,
            origin_config={
                "Id": f"{stack_name}-stac-api",
                "DomainName": stac_api_url,
                "OriginPath": "",
                "CustomHeaders": {"Quantity": 0},
                "CustomOriginConfig": {
                    "HTTPPort": 80,
                    "HTTPSPort": 443,
                    "OriginProtocolPolicy": "http-only",
                    "OriginSslProtocols": {"Quantity": 1, "Items": ["TLSv1.2"]},
                    "OriginReadTimeout": 60,
                    "OriginKeepaliveTimeout": 5,
                },
                "ConnectionAttempts": 3,
                "ConnectionTimeout": 10,
                "OriginShield": {"Enabled": False},
            },
            behavior_config={
                "PathPattern": f"{veda_cloudfront_settings.stac_path_prefix}*",
                "TargetOriginId": f"{stack_name}-stac-api",
                "TrustedSigners": {"Enabled": False, "Quantity": 0},
                "TrustedKeyGroups": {"Enabled": False, "Quantity": 0},
                "ViewerProtocolPolicy": "redirect-to-https",
                "AllowedMethods": {
                    "Quantity": 7,
                    "Items": [
                        "HEAD",
                        "DELETE",
                        "POST",
                        "GET",
                        "OPTIONS",
                        "PUT",
                        "PATCH",
                    ],
                    "CachedMethods": {"Quantity": 2, "Items": ["HEAD", "GET"]},
                },
                "SmoothStreaming": False,
                "Compress": True,
                "LambdaFunctionAssociations": {"Quantity": 0},
                "FunctionAssociations": {"Quantity": 0},
                "FieldLevelEncryptionId": "",
                "CachePolicyId": "4135ea2d-6df8-44a3-9df3-4b5a84be39ad",  # Managed CachingDisabled Policy
                "OriginRequestPolicyId": "216adef6-5c7f-47e4-b989-5492eafa07d3",  # Managed AllViewer Origin Request Policy
            },
        )

        # Raster API
        raster_cf = CloudfrontUpdate(
            self,
            "raster-api-cf-update",
            distribution_arn=veda_cloudfront_settings.cf_distribution_arn,
            origin_config={
                "Id": f"{stack_name}-raster-api",
                "DomainName": raster_api_url,
                "OriginPath": "",
                "CustomHeaders": {"Quantity": 0},
                "CustomOriginConfig": {
                    "HTTPPort": 80,
                    "HTTPSPort": 443,
                    "OriginProtocolPolicy": "http-only",
                    "OriginSslProtocols": {"Quantity": 1, "Items": ["TLSv1.2"]},
                    "OriginReadTimeout": 60,
                    "OriginKeepaliveTimeout": 5,
                },
                "ConnectionAttempts": 3,
                "ConnectionTimeout": 10,
                "OriginShield": {"Enabled": False},
            },
            behavior_config={
                "PathPattern": f"{veda_cloudfront_settings.raster_path_prefix}*",
                "TargetOriginId": f"{stack_name}-raster-api",
                "TrustedSigners": {"Enabled": False, "Quantity": 0},
                "TrustedKeyGroups": {"Enabled": False, "Quantity": 0},
                "ViewerProtocolPolicy": "redirect-to-https",
                "AllowedMethods": {
                    "Quantity": 7,
                    "Items": [
                        "HEAD",
                        "DELETE",
                        "POST",
                        "GET",
                        "OPTIONS",
                        "PUT",
                        "PATCH",
                    ],
                    "CachedMethods": {"Quantity": 2, "Items": ["HEAD", "GET"]},
                },
                "SmoothStreaming": False,
                "Compress": True,
                "LambdaFunctionAssociations": {"Quantity": 0},
                "FunctionAssociations": {"Quantity": 0},
                "FieldLevelEncryptionId": "",
                "CachePolicyId": "4135ea2d-6df8-44a3-9df3-4b5a84be39ad",  # Managed CachingDisabled Policy
                "OriginRequestPolicyId": "216adef6-5c7f-47e4-b989-5492eafa07d3",  # Managed AllViewer Origin Request Policy
            },
        )

        # they trigger sequentially and avoid collisions when calling the API
        raster_cf.resource.node.add_dependency(stac_cf.resource)

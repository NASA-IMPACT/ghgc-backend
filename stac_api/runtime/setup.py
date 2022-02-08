"""Setup stac_fastapi
Based on https://github.com/developmentseed/eoAPI/tree/master/src/eoapi/stac
"""

from setuptools import find_namespace_packages, setup

with open("README.md") as f:
    long_description = f.read()

inst_reqs = [
    "stac-fastapi.api~=2.3",
    "stac-fastapi.types~=2.3",
    "stac-fastapi.extensions~=2.3",
    "stac-fastapi.pgstac~=2.3",
    "jinja2>=2.11.2,<3.0.0",
    "starlette-cramjam>=0.1.0.a0,<0.2",
    "importlib_resources>=1.1.0;python_version<'3.9'",
]

extra_reqs = {
    "test": ["pytest", "pytest-cov", "pytest-asyncio", "requests"],
}


setup(
    name="delta.stac_api",  
    description=u"",
    python_requires=">=3.7",
    packages=find_namespace_packages(exclude=["tests*"]),
    package_data={"delta": ["stac/templates/*.html"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
)

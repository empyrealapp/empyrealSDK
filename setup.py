#!/usr/bin/env python
from setuptools import (
    setup,
)

with open("README.md") as f:
    readme = f.read()

extras_require = {
    "linter": [
        "black>=22.1.0",
        "flake8==3.8.3",
        "isort>=5.11.0",
        "mypy>=1.0.0",
        "types-setuptools>=57.4.4",
    ],
    "dev": [
        "pytest>=7.0.0",
        "pytest-asyncio>=0.18.1",
        "pytest-mock>=1.10",
        "pytest-watch>=4.2",
        "pytest-xdist>=1.29",
        "setuptools>=38.6.0",
    ],
}

setup(
    name="empyrealSDK",
    version="0.0.1.post3",
    description="Empyreal SDK for web3 development",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Empyreal",
    author_email="dev@empyreal.app",
    url="https://github.com/empyrealapp/empyrealSDK",
    install_requires=[
        "eth-typing>=3.0.0",
        "eth-utils>=2.1.0",
        "hexbytes>=0.1.0",
        "httpx>=0.23.3",
        "pydantic>=2.3.0",
    ],
    python_requires=">=3.7.2",
    extras_require=extras_require,
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

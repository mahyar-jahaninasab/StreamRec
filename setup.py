from setuptools import setup, find_packages

# Read dependencies from requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="streamrec",
    version="0.1.0",
    description="Streaming data collection and build datalake for online recommencations system toolkit using LLM to reinforce the user to but more products based on the sentitment analysis",
    author="Mahyar",
    author_email="jahaninasab.mahyar@gmail.com",
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=requirements,  
    license="MIT",
)

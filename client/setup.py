from setuptools import setup, find_packages
import os

# Read the requirements from requirements.txt
with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(
    name="client",
    version="0.1.0",
    packages=["client"],
    include_package_data=True,
    # Include all files in client/static
    package_data={
        'client': ['static/*']
    },
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'main=client.__main__:main',
        ],
    },
)

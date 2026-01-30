#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

# Extract central version information
with open(os.path.join(os.path.dirname(__file__), "VERSION")) as version_file:
    version = version_file.read().strip()

with open('requirements.txt') as f:
    requires = f.read().splitlines()

with open('README.md') as f:
    long_description = f.read()

setup(
    name="BEP032tools",
    version=version,
    packages=find_packages(),
    data_files=[('.', ['VERSION', 'README.md', 'requirements.txt'])],
    include_package_data=True,
    install_requires=[
        "pip~=23.2.1",
        "wheel~=0.41.2",
        "pytz~=2024.1",
        "PyYAML~=6.0.1",
        "numpy~=1.26.4",
        "setuptools~=68.2.0",
        "pandas~=2.2.2",
        "python-dateutil~=2.9.0.post0",
        "six~=1.16.0",
        "DigLabTools~=0.0.7",
	"elabapi_python~=5.0.2",
        "eye2bids @ git+https://github.com/bids-standard/eye2bids.git#egg=eye2bids"
    ],
    package_data={
            # If any package contains *.json or *.csv files, include them:
            "": ["*.json", '*.csv', '*.tsv', 'yml'],
'BIDSTools': [
            'ressources/schema/objects/*.yaml']
    },
    author="Jeremy Garcia, Sylvain Takerkart , Julia Sprenger",
    description="Checks the validity of a directory with respect to the BEP032 specifications ",
    long_description_content_type="text/markdown",
    long_description=long_description,
    license='MIT',

    entry_points={
        'console_scripts': ['BEP032Validator=bep032tools.validator.BEP032Validator:main',
                            'BEP032Generator=bep032tools.generator.BEP032Generator:main',
                            'BEP032Templater=bep032tools.generator.BEP032Templater:main',
                            'BEP032Viewer=bep032tools.viewer.BEP032Viewer:main',
                            'build-bids=BIDSTools.cli:cli'],
    },
    python_requires='>=3.10.12',
    extras_require={
        'tools': ['pandas', 'pynwb', 'neo', 'nixio'],
        'test': ['pytest', 'datalad', 'parameterized']
    }
)

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
    package_data={
            # If any package contains *.json or *.csv files, include them:
            "": ["*.json", '*.csv', '*.tsv'],
    },
    author="Jeremy Garcia, Sylvain Takerkart , Julia Sprenger",
    description="Checks the validity of a directory with respect to the BEP032 specifications ",
    long_description_content_type="text/markdown",
    long_description=long_description,
    license='MIT',
    install_requires=requires,
    entry_points={
        'console_scripts': ['BEP032Validator=bep032tools.validator.BEP032Validator:main',
                            'BEP032Generator=bep032tools.generator.BEP032Generator:main',
                            'BEP032Templater=bep032tools.generator.BEP032Templater:main',
                            'BEP032Viewer=bep032tools.viewer.BEP032Viewer:main'],
    },
    python_requires='>=3.7',
    extras_require={
        'tools': ['pandas', 'pynwb', 'neo', 'nixio'],
        'test': ['pytest', 'datalad']
    }
)

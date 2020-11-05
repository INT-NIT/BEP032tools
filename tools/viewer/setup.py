#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import subprocess

import re

verstr = "unknown"
try:
    verstrline = open('_version.py', "rt").read()
except EnvironmentError:
    pass # Okay, there is no version file.
else:
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        verstr = mo.group(1)
    else:
        raise RuntimeError("unable to find version in yourpackage/_version.py")


cmd = ['sudo','apt-get','install','tree']
print(' '.join(cmd))
subprocess.run(cmd)

setup(
    name="AnDOviewer",
    version=verstr,
    packages=find_packages(),
    author="Jeremy Garcia, Sylvain Takerkart",
    description="Little tools for ANimal Data Organization (ANDO) specifications ",
    license='MIT',
    install_requires=['flake8','pytest'],
    include_package_data=True,
    entry_points = {
        'console_scripts': ['AnDOviewer=AnDO_Viewer:main'],
    },
    python_requires='>=3.6',
)

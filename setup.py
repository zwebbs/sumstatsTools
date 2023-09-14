# File Name: setup.py
# Created By: ZW
# Created On: 2023-09-12
# Purpose: defines attributes and build specs for the python package

import setuptools

with open("README.md", 'r', encoding='utf-8') as fobj:
    long_description = fobj.read()

setuptools.setup(
    name="sumstatstools",
    version="0.1.2.1",
    author="Zach Weber",
    author_email="zach.weber.813@gmail.com",
    description="command line tools for working with GWAS summary stats",
    long_description=long_description,
    url="https://github.com/zwebbs/sumstatsTools",
    project_urls={
        "Bug Tracker" : "https://github.com/zwebbs/sumstatsTools/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[],
    entry_points={'console_scripts': {'sumstatsToVCF=scripts.sumstatsToVCF:main'}}
)


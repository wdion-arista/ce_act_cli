'''
# Unisntall pip
pip uninstall ce_act

# local build
python setup.py sdist bdist_wheel && \
pip install .

'''
from setuptools import setup, find_packages

with open('requirements-freeze.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="ce_act",
    version="1.0.5",
    packages=['ce_act', 'ce_act.service'],
    package_dir={'ce_act': 'ce_act'},
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ce_act=ce_act.__main__:main",
        ],
    },
)

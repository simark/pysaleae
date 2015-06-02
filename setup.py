from setuptools import setup

setup(
    name='pysaleae',
    version='0.1.0',
    author='Simon Marchi (simon.marchi@polymtl.ca)',
    packages=['saleae'],
    install_requires=['nose'],
    test_suite='nose.collector',
)

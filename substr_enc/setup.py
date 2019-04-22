"""
Substring-Searchable Encryption package setup.

Jiangchen Zhu  <zjcsjtu@umich.edu>
"""

from setuptools import setup

setup(
    name='substr_enc',
    version='0.1.2',
    packages=['substr_enc'],
    include_package_data=True,
    install_requires=[
        'pytest==4.3.0',
        'pycrypto==2.6.1'
    ]
)

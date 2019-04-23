"""
Substring-Searchable Encryption package setup.

Jiangchen Zhu  <zjcsjtu@umich.edu>
"""

from setuptools import setup

setup(
    name='substr_enc',
    version='0.1.4',
    packages=['substr_enc', 'substr_enc.enc', 'substr_enc.utils', 'substr_enc.conn'],
    include_package_data=True,
    install_requires=[
        'pytest==4.3.0',
        'pycryptodomex==3.8.1'
    ]
)

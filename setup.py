import os

from setuptools import find_packages
from setuptools import setup


cur_dir = os.path.dirname(__file__)
readme = os.path.join(cur_dir, 'README.md')
if os.path.exists(readme):
    with open(readme) as fh:
        long_description = fh.read()
else:
    long_description = ''

setup(
    name='func_cache',
    version=__import__('func_cache').__version__,
    description='func_cache',
    long_description=long_description,
    author='cary',
    author_email='cary@yunzujia.com',
    install_requires=['redis>=3.0.0'],
    packages=find_packages(exclude=['env']),
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='func_cache.tests',
)

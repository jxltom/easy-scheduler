import re
from setuptools import setup, find_packages

_version_re = r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]'

with open('easy_scheduler/__init__.py', 'r') as f:
    version = re.search(_version_re, f.read(), re.MULTILINE).group(1)

setup(
    name='easy-scheduler',
    version=version,
    packages=find_packages(),
    install_requires=['apscheduler'],

    author='jxltom',
    author_email='jxltom@gmail.com',
    license='MIT',
    keywords='apscheduler scheduling',
    url='https://github.com/jxltom/easy-scheduler/',
    description='Lightly encapsulated APScheduler for easier use',
)

#  python-grafannotate
#  ---------------
#  A CLI tool to add annotations to Grafana
#
#  Author:  Tim Birkett <tim.birkettdev@devopsmakers.com>
#  Website: https://github.com/devopsmakers/python-grafannotate
#  License: MIT License (see LICENSE file)

import codecs
from setuptools import find_packages, setup

dependencies = [
    'click==7.0',
    'requests==2.22.0',
    'influxdb==5.2.3'
]

setup(
    name='grafannotate',
    version='0.3.0',
    url='https://github.com/devopsmakers/python-grafannotate',
    license='MIT',
    author='Tim Birkett',
    author_email='tim.birkett@devopsmakers.com',
    description='Send annotations to Grafana',
    long_description=codecs.open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'grafannotate = grafannotate.cli:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)

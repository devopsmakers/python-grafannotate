#  python-publicholiday
#  ---------------
#  A fast, efficient command line utility for working with public holidays
#
#  Author:  Tim Birkett <tim.birkettdev@devopsmakers.com>
#  Website: https://github.com/devopsmakers/grafannotate
#  License: MIT License (see LICENSE file)

import codecs
from setuptools import find_packages, setup

dependencies = [
    'click==6.7',
    'requests==2.21.0'
]

setup(
    name='grafannotate',
    version='0.0.10',
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
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Topic :: Utilities',
        'Environment :: Console',
        #'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        #'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

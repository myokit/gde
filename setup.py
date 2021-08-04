#
# SetupTools script for GDE
#
# This file is part of GDE.
# See https://github.com/MichaelClerx/gde for sharing, and licensing details.
#
from setuptools import setup, find_packages


# Get version number
import os
import sys
sys.path.append(os.path.abspath('gde'))
from _gde_version import __version__ as version  # noqa
sys.path.pop()
del(os, sys)


# Load text for description
with open('README.md') as f:
    readme = f.read()


# Go!
setup(
    # Module name (lowercase)
    name='gde',

    # Version
    version=version,

    # Description
    description='Graph Data Exctractor (GDE)',
    long_description=readme,
    long_description_content_type='text/markdown',

    # License
    license='BSD 3-clause license',
    author='Michael Clerx',
    author_email='michael@myokit.org',

    # Required Python version
    python_requires='>=3.5',

    # Packages to include
    packages=find_packages(include=('gde', 'gde.*')),

    # Register as a shell script
    entry_points={
        'console_scripts': ['gde = gde.__main__:main']
    },

    # List of dependencies
    install_requires=[
        'configparser',
        'numpy',
        'pyqt5',
        'setuptools',
        'sip',
    ],

    # Classifiers for pypi
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
    ],
)

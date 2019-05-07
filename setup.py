"""Esal package definition and install configuration"""

# Copyright (c) 2018-2019 Aubrey Barnard.
#
# This is free software released under the MIT License.  See `LICENSE`
# for details.


import setuptools

import esal


# Extract the short and long descriptions from the documentation
_desc_paragraphs = esal.__doc__.strip().split('\n\n')
# Make sure to keep the short description to a single line
_desc_short = _desc_paragraphs[0].replace('\n', ' ')
# Include all the package documentation in the long description except
# for the first and last paragraphs which are the short description and
# the copyright notice, respectively
_desc_long = '\n\n'.join(_desc_paragraphs[1:-3])


# Define package attributes
setuptools.setup(

    # Basics
    name='esal',
    version=esal.__version__,
    url='https://github.com/afbarnard/esal',
    license='MIT',
    author='Aubrey Barnard',
    #author_email='',

    # Description
    description=_desc_short,
    long_description=_desc_long,
    keywords=[
        'event sequences',
        'data processing',
        'data analysis',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    platforms=['any'],

    # Requirements
    python_requires='>=3.4',
    install_requires=[], # No dependencies

    # API
    packages=setuptools.find_packages(),

)

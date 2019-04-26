#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
)

extras_require = {
    'test': [
        "pytest==3.3.2",
        "pytest-xdist",
        "pytest-asyncio==0.8.0",
        "tox>=2.9.1,<3",
    ],
    'lint': [
        "flake8==3.4.1",
        "isort>=4.2.15,<5",
        "mypy==0.701",
    ],
    'doc': [
        "Sphinx>=1.6.5,<2",
        "sphinx_rtd_theme>=0.1.9",
    ],
    'dev': [
        "bumpversion>=0.5.3,<1",
        "pytest-watch>=4.1.0,<5",
        "wheel",
        "twine",
        "ipython",
    ],
}

extras_require['dev'] = (
    extras_require['dev'] +
    extras_require['test'] +
    extras_require['lint'] +
    extras_require['doc']
)

setup(
    name='pytest-asyncio-network-simulator',
    # *IMPORTANT*: Don't manually change the version here. Use `make bump`, as described in readme
    version='0.1.0-alpha.2',
    description="""pytest-asyncio-network-simulator: Plugin for pytest for simulator the network in tests""",
    long_description_markdown_filename='README.md',
    author='Ethereum Foundation',
    author_email='piper@pipermerriam.com',
    url='https://github.com/ethereum/pytest-asyncio-network-simulator',
    include_package_data=True,
    install_requires=[
        "asyncio-cancel-token==0.1.0a2",
        # pytest 3.7.0 broke async fixtures.
        # https://github.com/pytest-dev/pytest-asyncio/issues/89
        "pytest>=3.3.2,<3.7.0",
        "pytest-asyncio>=0.8.0,<1",
    ],
    setup_requires=['setuptools-markdown'],
    python_requires='>=3.6, <4',
    extras_require=extras_require,
    py_modules=['pytest_asyncio_network_simulator'],
    license="MIT",
    zip_safe=False,
    keywords='asyncio network pytest',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'pytest11': ['pytest-asyncio-network-simulator=pytest_asyncio_network_simulator.plugin'],
    },
)

# pytest-asyncio-network-simulator

[![Join the chat at https://gitter.im/ethereum/pytest-asyncio-network-simulator](https://badges.gitter.im/ethereum/pytest-asyncio-network-simulator.svg)](https://gitter.im/ethereum/pytest-asyncio-network-simulator?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://circleci.com/gh/ethereum/pytest-asyncio-network-simulator.svg?style=shield)](https://circleci.com/gh/ethereum/pytest-asyncio-network-simulator)
[![PyPI version](https://badge.fury.io/py/pytest-asyncio-network-simulator.svg)](https://badge.fury.io/py/pytest-asyncio-network-simulator)
[![Python versions](https://img.shields.io/pypi/pyversions/pytest-asyncio-network-simulator.svg)](https://pypi.python.org/pypi/pytest-asyncio-network-simulator)
[![Docs build](https://readthedocs.org/projects/pytest-asyncio-network-simulator/badge/?version=latest)](http://pytest-asyncio-network-simulator.readthedocs.io/en/latest/?badge=latest)
   

A plugin for `pytest` which simulates the network in various `asyncio` APIs
such that rather than opening and communicating over sockets, communcation
happens directly in memory.

Read more in the [documentation on ReadTheDocs](https://pytest-asyncio-network-simulator.readthedocs.io/). [View the change log](https://pytest-asyncio-network-simulator.readthedocs.io/en/latest/releases.html).


## Quickstart

```sh
pip install pytest-asyncio-network-simulator
```

## Developer Setup

If you would like to hack on `pytest-asyncio-network-simulator`, please check out the
[Ethereum Development Tactical Manual](https://github.com/pipermerriam/ethereum-dev-tactical-manual)
for information on how we do:

- Testing
- Pull Requests
- Code Style
- Documentation

### Development Environment Setup

You can set up your dev environment with:

```sh
git clone git@github.com:ethereum/pytest-asyncio-network-simulator.git
cd pytest-asyncio-network-simulator
virtualenv -p python3 venv
. venv/bin/activate
pip install -e .[dev]
```

### Testing Setup

During development, you might like to have tests run on every file save.

Show flake8 errors on file change:

```sh
# Test flake8
when-changed -v -s -r -1 asyncio_network_simulator/ tests/ -c "clear; flake8 asyncio_network_simulator tests && echo 'flake8 success' || echo 'error'"
```

Run multi-process tests in one command, but without color:

```sh
# in the project root:
pytest --numprocesses=4 --looponfail --maxfail=1
# the same thing, succinctly:
pytest -n 4 -f --maxfail=1
```

Run in one thread, with color and desktop notifications:

```sh
cd venv
ptw --onfail "notify-send -t 5000 'Test failure ⚠⚠⚠⚠⚠' 'python 3 test on pytest-asyncio-network-simulator failed'" ../tests ../asyncio_network_simulator
```

### Release setup

For Debian-like systems:
```
apt install pandoc
```

To release a new version:

```sh
make release bump=$$VERSION_PART_TO_BUMP$$
```

#### How to bumpversion

The version format for this repo is `{major}.{minor}.{patch}` for stable, and
`{major}.{minor}.{patch}-{stage}.{devnum}` for unstable (`stage` can be alpha or beta).

To issue the next version in line, specify which part to bump,
like `make release bump=minor` or `make release bump=devnum`.

If you are in a beta version, `make release bump=stage` will switch to a stable.

To issue an unstable version when the current version is stable, specify the
new version explicitly, like `make release bump="--new-version 4.0.0-alpha.1 devnum"`

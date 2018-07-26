pytest asyncio network simulator
================================

.. warning:: This project should be considered alpha quality software.

This library can be used to transparently bypass the networking
component when testing ``asyncio`` applications.  This is accomplished by
monkeypatching various ``asyncio`` APIs to use locally connected stream readers
and writers instead of ones connected via a network.  The goal is for this to
be seamless, requiring no code changes in your application and a minimal
boilerplate in your test suite.

Contents
--------

.. toctree::
    :maxdepth: 3

    quickstart
    releases


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`

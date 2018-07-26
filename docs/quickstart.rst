Quickstart
==========


Installation
------------

Install with ``pip``

.. code-block:: bash

   $ pip install pytest-asyncio-network-simulator 


Patching ``asyncio``
--------------------

A pytest fixture is the easiest and quickest way to leverage this library.
Place the following either in a specific test module, or in a ``conftest.py``
file.

.. code-block:: bash

    import pytest

    @pytest.fixture(autouse=True)
    def network_sim(router):
        network = router.get_network(name='testing')
        with network.patch_asyncio():
            yield network


This will replace the following ``asyncio`` APIs with the patched versions.

* ``asyncio.open_connection``
* ``asyncio.start_server``


.. note::

    The `router` fixture used in the example above is provided by this library
    by default.

.. note:: 

    You can drop the ``autouse=True`` part from the fixture definition if you
    want to selectively include the fixture in your tests.

.. note::
    
    The `name='testing'` is arbitrary.  Any name will do.

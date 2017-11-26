==================================
Simple Async Web Server
==================================

Python asynchronous server example.

Key Features
============

- Server is written in python 3.6 and uses `aiohttp <http://aiohttp.readthedocs.io/en/stable/>`_ library.
- Easy to use `YAML <http://yaml.org/>`_ configuration files.
- Local and remote project deployment scripts are present.


Getting started
===============

.. code-block:: bash

    git clone git@github.com:kserhii/simple-async-server.git
    cd simple-async-server
    make setup
    ./runserver.py --config=dev

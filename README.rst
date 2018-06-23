Tickerqueue
===========
.. image:: https://travis-ci.com/kylegentle/tickerqueue.svg?branch=master
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black

A self-filling queue of cryptocurrency ticker data from public exchange APIs.

Basic Example
-------------

.. code-block:: python

   from tickerqueue import tickerqueue

   tq = tickerqueue('btc-eth')
   while True:
       ticker = tq.get()
       print(ticker)

Supported Exchanges
-------------------
- bittrex
- poloniex

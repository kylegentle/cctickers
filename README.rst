Tickerqueue
===========

A self-filling queue of cryptocurrency ticker data from public exchange APIs.

Basic Example
-------------

.. code-block:: python

   from tickerqueue import tickerqueue

   tq = tickerqueue('btc-eth')
   while True:
       print(tq.get())

Supported Exchanges
-------------------
- bittrex
- poloniex

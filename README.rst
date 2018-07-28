cctickers - Cryptocurrency tickers, aggregated
==============================================
.. image:: https://travis-ci.com/kylegentle/cctickers.svg?branch=master
   :target: https://travis-ci.com/kylegentle/cctickers

.. image:: https://codecov.io/gh/kylegentle/cctickers/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/kylegentle/cctickers

.. image:: https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg
   :target: https://opensource.org/licenses/MPL-2.0

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black

cctickers (pronounced "stickers") is a python package exposing a stream of aggregated cryptocurrency ticker data from public exchange APIs. *This package is under heavy development, and its API is subject to change. Use at your own risk.*

Usage
-------------
As a standalone package:

.. code-block:: bash

   cctickers btc-eth

Or, from your own python program:

.. code-block:: python

   from cctickers import tickerqueue

   with tickerqueue('btc-eth') as tq:
       while True:
           ticker = tq.get()
           print(ticker)

Supported Exchanges
-------------------
- binance
- bittrex
- poloniex

Example Output
--------------

.. code-block:: bash

   $ cctickers btc-eth

   timestamp=2018-06-23 19:25:37.719630    exchange=bittrex    pair=BTC-ETH    bid=0.076687    ask=0.07699996    last=0.076688
   timestamp=2018-06-23 19:25:37.769693    exchange=poloniex    pair=BTC-ETH    bid=0.07687165    ask=0.07693830    last=0.07687165
   timestamp=2018-06-23 19:25:37.880539    exchange=binance    pair=BTC-ETH    bid=0.07685900    ask=0.07692000    last=None
   timestamp=2018-06-23 19:25:38.191170    exchange=binance    pair=BTC-ETH    bid=0.07685900    ask=0.07692000    last=None
   timestamp=2018-06-23 19:25:38.497928    exchange=binance    pair=BTC-ETH    bid=0.07685900    ask=0.07692000    last=None
   timestamp=2018-06-23 19:25:38.690992    exchange=binance    pair=BTC-ETH    bid=0.07685900    ask=0.07692000    last=None
   timestamp=2018-06-23 19:25:38.753903    exchange=poloniex    pair=BTC-ETH    bid=0.07687165    ask=0.07693830    last=0.07687165
   timestamp=2018-06-23 19:25:38.776684    exchange=bittrex    pair=BTC-ETH    bid=0.076687    ask=0.07699996    last=0.076688

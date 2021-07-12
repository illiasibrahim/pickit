#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import urllib2

"""
Currency
========
    Currency Conversion, using openexangerates.org json API.
"""

__autor__ = 'Roberto Gea'
__version__ = '0.1'
__all__ = ('__version__', '__autor__', 'ExangeRates')


URL = 'http://openexchangerates.org'

#TODO: README
#TODO: CHANGES


class ExangeRates(object):
    """CurrencyExangeRates

    The exchange rates are updated hourly
    """

    def __init__(self, date=None):
        """
        Parameters:
        :param date:
        Historical exchange rate data are available for every day* since 1991
        (`datetime.date`)
        """
        self._url = URL
        self._date = date
        self._data = self._getjson()

    def _loadjson(self, filename):
        """Get json date"""
        jsonfile = urllib2.urlopen(self._url + '/' + filename)
        return json.loads(jsonfile.read())

    def _getjson(self):
        """Get all rates"""
        if self._date:
            date = self._date.strftime('%Y-%m-%d')
            return self._loadjson(
                    'historical/' + date + '.json')
        else:
            return self._loadjson('latest.json')

    def _tobase(self, ammount, currency):
        """Convert currency to base currency (USD)"""
        return ammount * float(self.rates[currency])

    @property
    def rates(self):
        """List of exange rates (USD based)"""
        return self._data['rates']

    @property
    def timestamp(self):
        """Latest update, or historical update"""
        return datetime.datetime.fromtimestamp(int(self._data['timestamp']))

    @property
    def base(self):
        """Base currency"""
        return  self._data['base'].upper()

    @property
    def currencies(self):
        """Get currency ISO codes"""
        return self._loadjson('currencies.json')

    def convert(self, ammount, currencyfrom, currencyto='USD'):
        """Convert currencies

        Parameters:
        :param ammount: ammount to convert
        :param currencyfrom: from currency (currency ISO codes)
        :param currencyto: to currency
        """
        usd = self._tobase(ammount, currencyto.upper())
        return usd / float(self.rates[currencyfrom.upper()])

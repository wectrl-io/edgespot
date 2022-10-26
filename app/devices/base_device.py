#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Base device class.
"""

from exceptions.exceptions import InvalidOption

class BaseDevice(object):
    """Base device class.
    """

    _options = {}
    """Options
    """

    _model = "Default Model"
    _vendor = "Default Vendor"

    @property
    def model(self):
        """Model

        Returns:
            string: Model
        """
        return self._model

    @property
    def vendor(self):
        """Vendor

        Returns:
            string: Vendor
        """
        return self._vendor

    @property
    def name(self):
        """Returns device name.

        Returns:
            str: Device name.
        """

        return self._get_option("name")

    def __str__(self):
        name = self._get_option("name")
        return f"name({name})/vendor({self.vendor})/model({self.model})"

    __repr__ = __str__

    def __init__(self, options, provider, adapter):

        if options is None:
            raise InvalidOption("Options is equal to None")

        self._options = options
        self._provider = provider
        self._adapter = adapter

    def _get_option(self, name, default=None):

        if name not in self._options and default is None:
            raise InvalidOption(f"Invalid option: {name}")

        if name not in self._options and default is not None:
            return default

        return self._options[name]


    def init(self):

        pass
    
    def update(self):

        pass
    
    def shutdown(self):

        pass
#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Base provider class.
"""

class BaseProvider(object):
    """Base provider class.
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

    def __str__(self):
        name = self._get_option("name")
        return f"name({name})/vendor({self.vendor})/model({self.model})"

    __repr__ = __str__

    def __init__(self, options):

        if options is None:
            raise Exception("Invalid options")

        self._options = options


    def _get_option(self, name, default=None):

        if name not in self._options and default is None:
            raise Exception(f"Invalid option: {name}")

        if name not in self._options and default is not None:
            return default

        return self._options[name]


    def get_data(self, data):

        return data

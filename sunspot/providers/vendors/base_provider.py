#!/usr/bin/env python3
# -*- coding: utf8 -*-

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = ""
"""Copyrighted"""

__credits__ = []
"""Credits"""

__license__ = ""
"""License
@see """

__version__ = "1.0.0"
"""Version of the file."""

__maintainer__ = ["Orlin Dimitrov", "Martin Maslyankov", "Nikola Atanasov"]
"""Name of the maintainer."""

__email__ = ""
"""E-mail of the author."""

__class_name__ = ""
"""Class name."""

#endregion

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
            raise ValueError("Invalid options")

        self._options = options


    def _get_option(self, name, default=None):

        if name not in self._options and default is None:
            raise ValueError(f"Invalid option: {name}")

        if name not in self._options and default is not None:
            return default

        return self._options[name]


    def get_data(self, data):

        return data

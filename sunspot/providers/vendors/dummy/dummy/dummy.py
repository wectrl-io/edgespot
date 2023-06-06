#!/usr/bin/env python3
# -*- coding: utf8 -*-

from providers.vendors.base_provider import BaseProvider

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

class Dummy(BaseProvider):
    """Dummy Provider
    """

    def __init__(self, options):
        """Constructor

        Args:
            options (dict): Options data.
        """

        super().__init__(options)
        self._vendor = "Dummy"
        self._model = "Dummy"

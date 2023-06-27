#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Providers factory
"""

from providers.vendors.dummy.dummy.dummy import Dummy
from providers.vendors.ebyte.nb114.nb114 import NB114
from providers.vendors.zlan.d_5143d.d_5143d import D_5143D
from providers.vendors.native.uart.uart import NativeUart

from exceptions.unsupported_provider import UnsupportedProvider

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

class ProvidersFactory(object):
    """Providers factory.
    """

    @staticmethod
    def create(settings):
        """Create master.

        Args:
            settings (dict): Settings data.

        Returns:
            Any: Instance of the master.
        """

        instance = None

        vendor = None
        if "vendor" not in settings:
            raise ValueError("Invalid vendor")
        else:
            vendor = settings["vendor"]

        model = None
        if "model" not in settings:
            raise ValueError("Invalid model")
        else:
            model = settings["model"]

        options = None
        if "options" not in settings:
            raise ValueError("Invalid options")
        else:
            options = settings["options"]

        if vendor == "dummy" and model == "dummy":
            instance = Dummy(options)

        elif vendor == "ebyte" and model == "nb114":
            instance = NB114(options)

        elif vendor == "zlan" and model == "5143d":
            instance = D_5143D(options)

        elif vendor == "native" and model == "uart":
            instance = NativeUart(options)

        else:
            raise UnsupportedProvider(f"Unsupported provider model({model}), vendor({vendor})")

        return instance

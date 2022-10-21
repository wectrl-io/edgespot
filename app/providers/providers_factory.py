#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Providers factory
"""

from providers.vendors.dummy.dummy.dummy import Dummy
from providers.vendors.ebyte.nb114.nb114 import NB114
from providers.vendors.native.uart.uart import NativeUart

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
            raise Exception("Invalid vendor")
        else:
            vendor = settings["vendor"]

        model = None
        if "model" not in settings:
            raise Exception("Invalid model")
        else:
            model = settings["model"]

        options = None
        if "options" not in settings:
            raise Exception("Invalid options")
        else:
            options = settings["options"]

        if vendor == "dummy" and model == "dummy":
            instance = Dummy(options)

        elif vendor == "ebyte" and model == "nb114":
            instance = NB114(options)

        elif vendor == "native" and model == "uart":
            instance = NativeUart(options)

        else:
            raise Exception(f"Unsupported provider model({model}), vendor({vendor})")

        return instance

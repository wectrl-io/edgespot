#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Devices factory class.
"""

from devices.vendors.dummy.dummy.dummy import Dummy
from devices.vendors.huawei.sun2000.sun2000 import SUN2000

class DevicesFactory:
    """Devices factory class.
    """

    @staticmethod
    def create(settings, provider, adapter):
        """Create device.

        Args:
            settings (dict): Settings data.

        Returns:
            Any: Instance of the device.
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
            instance = Dummy(options, provider, adapter)

        elif vendor == "huawei" and model == "sun2000":
            instance = SUN2000(options, provider, adapter)

        else:
            raise Exception(f"Unsupported device model({model}), vendor({vendor})")

        return instance

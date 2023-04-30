#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Devices factory class.
"""

from devices.vendors.cwt.mb308v.mb308v import CWTMB308V
from devices.vendors.dummy.dummy.dummy import Dummy
from devices.vendors.huawei.sun2000.sun2000 import SUN2000
from devices.vendors.nabu_casa.hass.hass import HomeAssistant
from devices.vendors.shelly.gen_1.shelly_1 import Shelly1
from devices.vendors.shelly.gen_1.shelly_1l import Shelly1L

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
            instance = Dummy(options, provider, adapter)

        elif vendor == "huawei" and model == "sun2000":
            instance = SUN2000(options, provider, adapter)

        elif vendor == "cwt" and model == "cwt_mb308v":
            instance = CWTMB308V(options, provider, adapter)

        elif vendor == "nabu_casa" and model == "hass":
            instance = HomeAssistant(options, provider, adapter)

        elif vendor == "alterco" and model == "shelly1":
            instance = Shelly1(options, provider, adapter)

        elif vendor == "alterco" and model == "shelly1l":
            instance = Shelly1L(options, provider, adapter)

        else:
            raise Exception(f"Unsupported device model({model}), vendor({vendor})")

        return instance

#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Devices factory class.
"""

from devices.vendors.cwt.mb308v.mb308v import CWTMB308V

from devices.vendors.dummy.dummy.dummy import Dummy

from devices.vendors.huawei.sun2000.sun2000 import SUN2000

from devices.vendors.nabu_casa.hass.hass import HomeAssistant

from devices.vendors.shelly.gen_1.http.shelly_1 import Shelly1
from devices.vendors.shelly.gen_1.http.shelly_1l import Shelly1L
from devices.vendors.shelly.gen_1.http.shelly_2 import Shelly2
from devices.vendors.shelly.gen_1.http.shelly_2p5 import Shelly2p5
from devices.vendors.shelly.gen_1.http.shelly_em import ShellyEM
from devices.vendors.shelly.gen_1.http.shelly_3em import Shelly3EM
from devices.vendors.shelly.gen_2.http.shelly_plus_1 import ShellyPlus1

from devices.vendors.eastron.sdm120.sdm120 import SDM120

from devices.vendors.donkger.xy_md02.xy_md02 import XY_MD02

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

        if "name" not in settings:
            raise ValueError("Invalid name")
        else:
            options["name"] = settings["name"]

        if vendor == "dummy" and model == "dummy":
            instance = Dummy(options, provider, adapter)

        elif vendor == "huawei" and model == "sun2000":
            instance = SUN2000(options, provider, adapter)

        elif vendor == "cwt" and model == "cwt_mb308v":
            instance = CWTMB308V(options, provider, adapter)

        elif vendor == "nabu_casa" and model == "hass":
            instance = HomeAssistant(options, provider, adapter)

        elif vendor == "alterco" and model == "shelly_1_gen1":
            instance = Shelly1(options, provider, adapter)

        elif vendor == "alterco" and model == "shelly_1l_gen1":
            instance = Shelly1L(options, provider, adapter)

        elif vendor == "alterco" and model == "shelly_2_gen1":
            instance = Shelly2(options, provider, adapter)

        elif vendor == "alterco" and model == "shelly_2p5_gen1":
            instance = Shelly2p5(options, provider, adapter)

        elif vendor == "alterco" and model == "shelly_em_gen1":
            instance = ShellyEM(options, provider, adapter)

        elif vendor == "alterco" and model == "shelly_3em_gen1":
            instance = Shelly3EM(options, provider, adapter)

        elif vendor == "alterco" and model == "shelly_plus_1_gen2":
            instance = ShellyPlus1(options, provider, adapter)

        elif vendor == "eastron" and model == "sdm120":
            instance = SDM120(options, provider, adapter)

        elif vendor == "donkger" and model == "xy-md02":
            instance = XY_MD02(options, provider, adapter)

        else:
            raise NotImplementedError(f"Unsupported device model({model}), vendor({vendor})")

        return instance

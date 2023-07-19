#!/usr/bin/env python3
# -*- coding: utf8 -*-

import json

from utils.logger import get_logger
from utils.timer import Timer

from .shelly_http_base import ShellyHttpBase

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

class ShellyPlus1(ShellyHttpBase):

#region Attributes

    __logger = None
    """Logger
    """

    __timer = None
    """Update timer.
    """

    __update_period = 1
    """Update period.
    """

#endregion

#region Constructor

    def __init__(self, options, provider, adapter):
        """Constructor

        Args:
            options (dict): Instance options.
            provider (object): Data provider.
            adapter (object): Adapter collector.
        """

        super().__init__(options, provider, adapter)
        self._vendor = "Alterco"
        self._model = "ShellyPlus1-GEN2"

#endregion

#region Public Methods (API)

#endregion

#region Private Methods

    def __timer_cb(self, timer):

        timer.clear()

        device_status = self.status()

        # print(device_status["wifi_sta"])

        if device_status is not None:
            for realm in device_status:
                self._adapter.pub_attribute("status", realm, self.name, json.dumps(device_status[realm]))

        # self._adapter.pub_attribute("realm_name", "attribute_name", "asset_id", "Hello, world.")

        # self._adapter.send_telemetry(data)

        # self.__logger.info("Working process")

#endregion

#region Public Methods

    async def init(self):

        # Set logger.
        self.__logger = get_logger(__name__)

        # Set timer. (Default value is 1 second.)
        update_period = self._get_option("update_period", 1)
        update_period = float(update_period)
        self.__update_period = update_period
        self.__timer = Timer(self.__update_period)
        self.__timer.set_callback(self.__timer_cb)

        await self._adapter.connect()

    async def update(self):

        await self.__timer.update()
        await self._adapter.update()

    async def shutdown(self):

        self._adapter.disconnect()

#endregion

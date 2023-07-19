#!/usr/bin/env python3
# -*- coding: utf8 -*-

import random
import json

from utils.logger import get_logger
from utils.timer import Timer

from devices.base_device import BaseDevice

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

class Dummy(BaseDevice):
    """Dummy Device
    """

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
            options (dict): Options data.
        """

        super().__init__(options, provider, adapter)
        self._vendor = "Dummy"
        self._model = "Dummy"

        # Set logger.
        self.__logger = get_logger(__name__)

        # Set timer. (Default value is 1 second.)
        update_period = self._get_option("update_period", 1)
        update_period = float(update_period)
        self.__update_period = update_period
        self.__timer = Timer(self.__update_period)
        self.__timer.set_callback(self.__timer_cb)

#endregion

#region Private Methods

    def __get_params(self):

        return {"value1": random.randint(0, 9), "value2": random.randint(0, 9)}

    def __timer_cb(self, timer):

        timer.clear()

        params = self.__get_params()

        data = self._provider.get_data(params)
        dumps = json.dumps(data)
        enc_dumps = dumps.encode("utf-8")
        self._adapter.pub_attribute("realm_name", "attribute_name", self.name, enc_dumps)

        # self._adapter.send_telemetry(data)

        # self.__logger.info("Working process")

#endregion

#region Public Methods

    async def init(self):

        await self._adapter.connect()

    async def update(self):

        await self.__timer.update()
        await self._adapter.update()

    async def shutdown(self):

        self._adapter.disconnect()

#endregion

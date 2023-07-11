#!/usr/bin/env python3
# -*- coding: utf8 -*-

import json
import random

from devices.base_device import BaseDevice
from utils.logger import get_logger
from utils.timer import Timer

from huawei_solar import AsyncHuaweiSolar, register_names as rn

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

class SUN2000(BaseDevice):
    """Huawei SUN2000 device.
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

    __bridge = None

    __host = ""

    __port = 502

#endregion

#region Constructor

    def __init__(self, options, provider, adapter):
        """Constructor

        Args:
            options (dict): Options data.
        """

        super().__init__(options, provider, adapter)
        self._vendor = "Huawei"
        self._model = "SUN2000"

#endregion

#region Private Methods

    def __timer_cb(self, timer):

        timer.clear()

        # self.__logger.info("Working process")

        print(self.__bridge.update())

    def __callback(self, client, userdata, message):

        # Log message.
        self.__logger.info(\
            f"Topic: {message.topic}; Message: {message.payload}")

        # Decode JSON request
        data = json.loads(message.payload)

        # # Check request method
        # if data['method'] == 'getGpioStatus':
        #     # Reply with GPIO status.
        #     client.publish(message.topic.replace('request', 'response'), self.__get_gpio_status(), 1)

        # elif data['method'] == 'setGpioStatus':
        #     # Update GPIO status and reply.
        #     self.__set_gpio_status(data['params']['pin'], data['params']['enabled'])
        #     client.publish(message.topic.replace('request', 'response'), self.__get_gpio_status(), 1)
        #     client.publish('v1/devices/me/attributes', self.__get_gpio_status(), 1)

        #     # TODO: Send data thought the provider to the IO island.
        #     self._provider

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

        self.__host = self._get_option("host", "192.168.113.114")
        self.__port = self._get_option("port", 502)

    async def update(self):

        if self.__bridge is None:
            self.__bridge = await HuaweiSolarBridge.create(host=self.__host, port=self.__port)

        if self.__timer is not None:
            self.__timer.update()

    def shutdown(self):

        pass

#endregion

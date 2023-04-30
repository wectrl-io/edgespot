#!/usr/bin/env python3
# -*- coding: utf8 -*-

import json

from utils.logger import get_logger
from utils.timer import Timer

from .shelly_http_base import ShellyHttpBase

class Shelly1L(ShellyHttpBase):

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
        self._model = "Shgelly1L-GEN1"

        # Set logger.
        self.__logger = get_logger(__name__)

        # Set timer.
        self.__timer = Timer(self.__update_period)
        self.__timer.set_callback(self.__timer_cb)

#endregion

#region Public Methods (API)

    def relay(self, index=0, turn="off"):
        """Get status from the device.

        Args:
            index (int, optional): _description_. Defaults to 0.
            turn (str, optional): _description_. Defaults to "off".
        """

        url = f"{self._base_url}/relay/{index}?turn={turn}"
        return self._get_requests(url)

    def settings_relay(self, index=0):
        """Get settings relay from the device.

        Args:
            index (int, optional): Chanel index. Defaults to 0.

        Returns:
            dict: Device response.
        """

        url = f"{self._base_url}/settings/relay/{index}"
        return self._get_requests(url)

    def settings_power(self, index=0):
        """Get settings power from the device.

        Args:
            index (int, optional): Chanel index. Defaults to 0.

        Returns:
            dict: Device response.
        """

        url = f"{self._base_url}/settings/power/{index}"
        return self._get_requests(url)

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

    def init(self):

        self._adapter.connect()

    def update(self):

        self.__timer.update()
        self._adapter.update()

    def shutdown(self):

        self._adapter.disconnect()

#endregion
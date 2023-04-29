#!/usr/bin/env python3
# -*- coding: utf8 -*-

import random
from utils.timer import Timer
from utils.logger import get_logger
from devices.base_device import BaseDevice

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

        # Set timer.
        self.__timer = Timer(self.__update_period)
        self.__timer.set_callback(self.__timer_cb)

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

#region Private Methods

    def __get_params(self):

        return {"value1": random.randint(0, 9), "value2": random.randint(0, 9)}

    def __timer_cb(self, timer):

        timer.clear()

        params = self.__get_params()

        data = self._provider.get_data(params)

        self._adapter.pub_attribute("realm_name", "attribute_name", "asset_id", "Hello, world!")

        # self._adapter.send_telemetry(data)

        # self.__logger.info("Working process")

#endregion
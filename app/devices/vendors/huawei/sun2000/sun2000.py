#!/usr/bin/env python3
# -*- coding: utf8 -*-

import json
import random

from devices.base_device import BaseDevice
from utils.logger import get_logger
from utils.timer import Timer

class SUN2000(BaseDevice):
    """Huawei SUN2000 device.
    """

#region Attributes

    __logger = None
    """Logger
    """

    __gpio_state = {\
        7: False, 11: False, 12: False, 13: False,\
        15: False, 16: False, 18: False, 22: False,\
        29: False, 31: False, 32: False, 33: False,\
        35: False, 36: False, 37: False, 38: False, 40: False}

    __update_period = 1

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

    def __timer_cb(self, timer):

        timer.clear()

        params = {
            "value1": random.randint(0, 9),
            "value2": random.randint(0, 9),
            "value3": self.__gpio_state[7] * 10}\
            # Add feedback for visual fun! Only for party purpose.

        # data = self._provider.get_data(params)

        self._adapter.send_telemetry(params)

        # self.__logger.info("Working process")

    def __get_gpio_status(self):

        return json.dumps(self.__gpio_state)

    def __set_gpio_status(self, pin, status):

        # Update GPIOs state.
        self.__gpio_state[pin] = status

    def __callback(self, client, userdata, message):

        # Log message.
        self.__logger.info(\
            f"Topic: {message.topic}; Message: {message.payload}")

        # Decode JSON request
        data = json.loads(message.payload)

        # Check request method
        if data['method'] == 'getGpioStatus':
            # Reply with GPIO status.
            client.publish(message.topic.replace('request', 'response'), self.__get_gpio_status(), 1)

        elif data['method'] == 'setGpioStatus':
            # Update GPIO status and reply.
            self.__set_gpio_status(data['params']['pin'], data['params']['enabled'])
            client.publish(message.topic.replace('request', 'response'), self.__get_gpio_status(), 1)
            client.publish('v1/devices/me/attributes', self.__get_gpio_status(), 1)

            # TODO: Send data thought the provider to the IO island.
            self._provider

#endregion

#region Public Methods

    def init(self):

        self._adapter.connect()
        self._adapter.subscribe(gpio_state=self.__get_gpio_status, callback=self.__callback)

    def update(self):

        self.__timer.update()
        self._adapter.update()

    def shutdown(self):

        self._adapter.disconnect()

#endregion

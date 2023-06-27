#!/usr/bin/env python3
# -*- coding: utf8 -*-

import json
import random
import time

from devices.base_device import BaseDevice
from utils.timer import Timer
from utils.logger import get_logger

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

class CWTMB308V(BaseDevice):
    """CWTMB308V"""

#region Attributes

    __logger = None
    """Logger
    """

    __gpio_state = {\
        7: False, 11: False, 12: False, 13: False,\
        15: False, 16: False, 18: False, 22: False,\
        29: False, 31: False, 32: False, 33: False,\
        35: False, 36: False, 37: False, 38: False, 40: False}

    __update_period = 60

#endregion

#region Constructor

    def __init__(self, options, provider, adapter):
        """Constructor

        Args:
            options (dict): Options data.
        """

        super().__init__(options, provider, adapter)
        self._vendor = "cwt"
        self._model = "mb_308v"

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

        # Clear the timer.
        timer.clear()

        # Get device modbus ID.
        unit = self._get_option("modbus_id")

        # Get communicator.
        client = self._provider.communicator

        # Connect to the communicator.
        client.connect()

        # Create parameters.
        parameters = {}

        # TODO: Create interface way to send information to the adapters!!!

        # Read discrete inputs.
        rr = client.read_coils(0, 12, unit)
        if not rr.isError():
            for index in range(0, 12):
                key = f"RO{index}"
                parameters[key] = 1 if rr.bits[index] else 0

        # Read discrete inputs.
        rr = client.read_discrete_inputs(0, 8, unit)
        if not rr.isError():
            for index in range(0, 8):
                key = f"DI{index}"
                parameters[key] = 1 if rr.bits[index] else 0

        # Read analog inputs.
        rr = client.read_input_registers(0, 8, unit)
        if not rr.isError():
            for index in range(0, 8):
                key = f"AI{index}"
                parameters[key] = rr.registers[index]

        # Read analog outputs.
        rr = client.read_holding_registers(0, 4, unit)
        if not rr.isError():
            for index in range(0, 4):
                key = f"AO{index}"
                parameters[key] = rr.registers[index]

        
        for parameter in parameters:
            self._adapter.pub_attribute("gpio_bi", parameter, self.name, json.dumps(parameters[parameter]))


        # self.__logger.debug(f"Data: {parameters}")

        # Send data to the cloud.
        # self._adapter.send_telemetry(parameters)

    def __get_gpio_status(self):

        return json.dumps(self.__gpio_state)

    def __set_gpio_status(self, pin, status):

        # Update GPIOs state.
        self.__gpio_state[pin] = status

    def __on_message(self, client, userdata, message):

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

            self.__update_do_ro()

    def __update_do_ro(self):
        states = []
        for gpio, state in self.__gpio_state.items():
            states.append(state)

        client = self._provider.communicator
        unit = self._get_option("modbus_id")
        client.connect()
        client.write_coils(0, states, unit)
        client.close()

#endregion

#region Public Methods

    def init(self):

        self._adapter.connect()
        # self._adapter.subscribe(gpio_state=self.__get_gpio_status, callback=self.__on_message)

    def update(self):

        self.__timer.update()
        self._adapter.update()

    def shutdown(self):

        self._adapter.disconnect()

#endregion

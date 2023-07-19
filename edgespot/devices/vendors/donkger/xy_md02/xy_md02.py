#!/usr/bin/env python3
# -*- coding: utf8 -*-

import json
import random
import time

from devices.base_device import BaseDevice
from data.modbus.function_code import FunctionCode
from data.modbus.parameter import Parameter
from data.modbus.parameter_type import ParameterType
from data.modbus.converter import Converter
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

class XY_MD02(BaseDevice):
    """Donkger XY-MD02"""

#region Attributes

    __logger = None
    """Logger
    """

    __update_period = 60

    _parameters = []

#endregion

#region Constructor

    def __init__(self, options, provider, adapter):
        """Constructor

        Args:
            options (dict): Options data.
        """

        super().__init__(options, provider, adapter)
        self._vendor = "Donkger"
        self._model = "XY-MD02"

#endregion

#region Private Methods

    def __setup_registers(self):

        self._parameters.append(
            Parameter("Temperature", "ºC",
            ParameterType.UINT16_T, [1], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Humidity", "Rh",
            ParameterType.UINT16_T, [2], FunctionCode.ReadInputRegisters))

    def __timer_cb(self, timer):

        # Clear the timer.
        timer.clear()

        # Get device modbus ID.
        unit = self._get_option("modbus_id")

        # Get communicator.
        client = self._provider.communicator

        # Connect to the communicator.
        client.connect()

        # TODO: Create interface way to send information to the adapters!!!

        # # Read discrete inputs.
        # rr = client.read_coils(0, 12, unit)
        # if not rr.isError():
        #     for index in range(0, 12):
        #         key = f"RO{index}"
        #         parameters[key] = 1 if rr.bits[index] else 0

        # # Read discrete inputs.
        # rr = client.read_discrete_inputs(0, 8, unit)
        # if not rr.isError():
        #     for index in range(0, 8):
        #         key = f"DI{index}"
        #         parameters[key] = 1 if rr.bits[index] else 0

        # Read analog inputs.
        # rr = client.read_input_registers(0, 2, unit)
        # if not rr.isError():
        #     for index in range(0, 2):
        #         key = f"IR{index}"
        #         parameters[key] = rr.registers[index]

        # # Read analog outputs.
        # rr = client.read_holding_registers(0, 4, unit)
        # if not rr.isError():
        #     for index in range(0, 4):
        #         key = f"AO{index}"
        #         parameters[key] = rr.registers[index]

        for param in self._parameters:
            # Read analog inputs.
            rr = client.read_input_registers(min(param.addresses), len(param.addresses), unit)
            if not rr.isError():
                value = Converter.convert(param.data_type, [0, 1], rr.registers)

                if value is not None:
                    value = value / 10.0

                self._adapter.pub_attribute("PTS", self.name, param.name, str(value))

        client.close()

    def __on_message(self, client, userdata, message):

        # Log message.
        self.__logger.info(\
            f"Topic: {message.topic}; Message: {message.payload}")

        # Decode JSON request
        data = json.loads(message.payload)

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

        self.__setup_registers()

        await self._adapter.connect()
        # self._adapter.subscribe(gpio_state=self.__get_gpio_status, callback=self.__on_message)

    async def update(self):

        await self.__timer.update()
        await self._adapter.update()

    async def shutdown(self):

        self._adapter.disconnect()

#endregion

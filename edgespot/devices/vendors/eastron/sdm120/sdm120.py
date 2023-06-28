#!/usr/bin/env python3
# -*- coding: utf8 -*-

import json
import random
import time

from edgespot.devices.base_device import BaseDevice
from edgespot.data.modbus.function_code import FunctionCode
from edgespot.data.modbus.parameter import Parameter
from edgespot.data.modbus.parameter_type import ParameterType
from edgespot.data.modbus.converter import Converter
from edgespot.utils.timer import Timer
from edgespot.utils.logger import get_logger

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

class SDM120(BaseDevice):
    """Eastron SDM120"""

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
        self._vendor = "Easteron"
        self._model = "SDM120"

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

    def __setup_registers(self):

        self._parameters.append(
            Parameter("Voltage", "V",
            ParameterType.FLOAT, [0, 1], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Current", "A",
            ParameterType.FLOAT, [6, 7], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("ActivePower", "W",
            ParameterType.FLOAT, [12, 13], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("ApparentPower", "VA",
            ParameterType.FLOAT, [18, 19], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("ReactivePower", "VAr",
            ParameterType.FLOAT, [24, 25], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("PowerFactor", "DEG",
            ParameterType.FLOAT, [30, 31], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Frequency", "Hz",
            ParameterType.FLOAT, [70, 71], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("ImportActiveEnergy", "kWr",
            ParameterType.FLOAT, [72, 73], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("ExportActiveEnergy", "kWr",
            ParameterType.FLOAT, [74, 75], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("ImportReactiveEnergy", "kvarh",
            ParameterType.FLOAT, [76, 77], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("ExportReactiveEnergy", "kvarh",
            ParameterType.FLOAT, [78, 79], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalSystemPowerDemand", "W",
            ParameterType.FLOAT, [84, 85], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("MaximumTotalSystemPowerDemand", "W",
            ParameterType.FLOAT, [86, 87], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("ImportSystemPowerDemand", "W",
            ParameterType.FLOAT, [88, 89], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("MaximumImportSystemPowerDemand", "W",
            ParameterType.FLOAT, [90, 91], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("ExportSystemPowerDemand", "W",
            ParameterType.FLOAT, [92, 93], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("MaximumExportSystemPowerDemand", "W",
            ParameterType.FLOAT, [94, 95], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("CurrentDemand", "A",
            ParameterType.FLOAT, [258, 259], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("MaximumCurrentDemand", "A",
            ParameterType.FLOAT, [264, 265], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalActiveEnergy", "kWh",
            ParameterType.FLOAT, [342, 343], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalReactiveEnergy", "kVArh",
            ParameterType.FLOAT, [344, 345], FunctionCode.ReadInputRegisters))


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

    def init(self):

        self.__setup_registers()

        self._adapter.connect()
        # self._adapter.subscribe(gpio_state=self.__get_gpio_status, callback=self.__on_message)

    def update(self):

        self.__timer.update()
        self._adapter.update()

    def shutdown(self):

        self._adapter.disconnect()

#endregion

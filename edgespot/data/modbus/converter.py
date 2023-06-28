#!/usr/bin/env python3
# -*- coding: utf8 -*-

from enum import Enum
from struct import pack, unpack

from edgespot.data.modbus.parameter_type import ParameterType

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

class Converter():

    @staticmethod
    def convert(parameter_type, registers, registers_data):
        """Convert registers data to a single parameter.

        Parameters
        ----------
        parameter_type : ParameterType
            Data type.
        registers : array
            Registers addresses.
        registers_data : array
            Registers data.

        Returns
        -------
        float
            Parameter value.
        """

        if ParameterType.is_valid(parameter_type) is not True:
            raise ValueError("Modbus data type mismatch.")

        if not registers:
            raise Exception("Invalid registers length.")

        if len(registers_data) <= 0:
            raise Exception("Registers content length can not be 0.")

        #/** @var object Unpacked float value. value */
        value = None

        if parameter_type == ParameterType.INT16_T:
            value = registers_data[registers[0]]

        elif parameter_type == ParameterType.UINT16_T:
            value = registers_data[registers[0]]

        elif parameter_type == ParameterType.INT32_T:
            raise NotImplemented("Not implemented")

        elif parameter_type == ParameterType.UINT32_T:
            raise NotImplemented("Not implemented")

        elif parameter_type == ParameterType.FLOAT:
            #/** @var array Packet binary data. bin_data */
            bin_data = None
            bin_data = pack(
                "<HH",
                registers_data[registers[1]],
                registers_data[registers[0]])
            value = unpack("f", bin_data)[0]

        return value

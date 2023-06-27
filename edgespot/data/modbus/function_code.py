#!/usr/bin/env python3
# -*- coding: utf8 -*-

from enum import Enum

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

class FunctionCode(Enum):
    """Register type"""

    ReadCoil = 1
    ReadDiscreteInput = 2
    ReadHoldingRegisters = 3
    ReadInputRegisters = 4
    WriteSingleCoil = 5
    WriteSingleHoldingRegister = 6
    WriteMultipleCoils = 15
    WriteMultipleHoldingRegisters = 16

    @staticmethod
    def is_valid(data_type):
        """Checks is the data type is valid."""

        state = False

        for function_code in FunctionCode:
            if data_type == function_code.value:
                state = True
                break

        return state
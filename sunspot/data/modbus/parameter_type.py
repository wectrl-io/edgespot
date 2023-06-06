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

class ParameterType(Enum):
    """Parameter data type enumeration class."""

    UINT16_T = "uint16_t"
    INT16_T = "int16_t"
    UINT32_T = "uint32_t"
    INT32_T = "int32_t"
    UINT64_T = "uint64_t"
    INT64_T = "int64_t"
    FLOAT = "float"
    STRING = "string"
    REAL = "real"

#region Public static Methods

    @staticmethod
    def is_valid(value):
        """Check validity of the data type.

        Args:
            value (str): Target data type for check.

        Return:
            bool: Valid data type.
        """
        state = False

        for item in ParameterType:
            if value == item:
                state = True
                break

        return state

#endregion
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

class Parameter:
    """Modbus parameter descriptor."""

#region Attributes

    __parameter_name = "Parameter"
    """Parameter name."""

    __mou = "Unit"
    """Measure of unit."""

    __data_type = ""
    """Data type."""

    __addresses = []
    """Modbus addresses."""

    __function_code = ""
    """Register type."""

    __limits = []
    """Limits."""    

#endregion

#region Getters and Setters

    @property
    def name(self):
        """Parameter name."""

        return self.__parameter_name

    @name.setter
    def name(self, name):
        """Parameter name.

        Args:
            name (string): Parameter name.
        """
        self.__parameter_name = name

    @property
    def mou(self):
        """Unit of measurement."""

        return self.__mou

    @mou.setter
    def mou(self, mou):
        """Unit of measurement.

        Args:
            mou (string): Unit of measurement.
        """

        self.__mou = mou

    @property
    def data_type(self):
        """Data type

        Return:
            addresses (list): Data type.
        """
        return self.__data_type

    @data_type.setter
    def data_type(self, data_type):
        """Data type

        Args:
            data_type (string): Data type.
        """

        self.__data_type = data_type

    @property
    def addresses(self):
        """addresses

        Return:
            addresses (list): addresses.
        """

        return self.__addresses

    @addresses.setter
    def addresses(self, addresses):
        """addresses

        Args:
            addresses (list): addresses.
        """

        self.__addresses = addresses

    @property
    def function_code(self):
        """Register type."""

        return self.__function_code

    @function_code.setter
    def function_code(self, function_code):
        """Register type.

        Args:
            function_code (string): Register type.
        """

        self.__function_code = function_code

    @property
    def limits(self):
        """Limits"""

        return self.__limits

    @limits.setter
    def limits(self, limits):
        """Limits

        Args:
            limits (list): Limits values.
        """

        self.__limits = limits

#endregion

#region Constructor

    def __init__(self, name, mou, data_type, addresses, function_code, limits=[0, 100]):
        """Constructor

        Args:
            name (string): Parameter name..
            mou (string): Measure of unit.
            data_type (string): Data type.
            addresses (list): Modbus addresses.
            function_code (string)
        """

        self.name = name
        self.mou = mou
        self.data_type = data_type
        self.addresses = addresses
        self.function_code = function_code
        self.limits = limits

#endregion

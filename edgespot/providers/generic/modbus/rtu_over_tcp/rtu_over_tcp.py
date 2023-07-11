#!/usr/bin/env python3
# -*- coding: utf8 -*-

from providers.vendors.base_provider import BaseProvider

from pymodbus.client.tcp import ModbusTcpClient as ModbusClient
# from pymodbus.transaction import ModbusSocketFramer as ModbusFramer

from pymodbus.transaction import ModbusRtuFramer
from pymodbus.transaction import ModbusBinaryFramer
from pymodbus.transaction import ModbusAsciiFramer

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

class RtuOverTcp(BaseProvider):
    """RTU overTCP master device.
    """

#region Attributes

    __client = None
    """Modbus Master
    """

#endregion

#region Properties

    @property
    def communicator(self):
        """Communicator instance.

        Returns:
            Any: Communicator instance.
        """

        return self.__client

#endregion

#region Constructor

    def __init__(self, options):
        """Constructor

        Args:
            options (dict): Options data.
        """
        super().__init__(options)
        self._vendor = "EByte"
        self._model = "NB114"

        ip = self._get_option("ip")
        port = self._get_option("port")
        framer_type = self._get_option("framer_type")
        framer = self.__get_framer(framer_type)

        self.__client = ModbusClient(ip, port=port, framer=framer)

#endregion

#region Private Methods

    def __get_framer(self, framer_type):

        framer = None

        if framer_type == "rtu":
            framer = ModbusRtuFramer
        elif framer_type == "bin":
            framer = ModbusBinaryFramer
        elif framer_type == "ascii":
            framer = ModbusAsciiFramer
        else:
            raise ValueError(f"Unsupported framer type({framer_type})")
        return framer

#endregion

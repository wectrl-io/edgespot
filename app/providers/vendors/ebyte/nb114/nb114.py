#!/usr/bin/env python3
# -*- coding: utf8 -*-

from providers.vendors.base_provider import BaseProvider

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
# from pymodbus.transaction import ModbusSocketFramer as ModbusFramer

from pymodbus.transaction import ModbusRtuFramer
from pymodbus.transaction import ModbusBinaryFramer
from pymodbus.transaction import ModbusAsciiFramer

class NB114(BaseProvider):
    """NB114 master device.
    """

    __client = None
    """Modbus Master
    """

    @property
    def communicator(self):
        """Communicator instance.

        Returns:
            Anu: Communicator instance.
        """

        return self.__client

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

    def __get_framer(self, framer_type):

        framer = None

        if framer_type == "rtu":
            framer = ModbusRtuFramer
        elif framer_type == "bin":
            framer = ModbusBinaryFramer
        elif framer_type == "ascii":
            framer = ModbusAsciiFramer
        else:
            raise Exception(f"Unsupported framer type({framer_type})")
        return framer

#!/usr/bin/env python3
# -*- coding: utf8 -*-

from providers.vendors.base_provider import BaseProvider

from pymodbus.client.serial import ModbusSerialClient as ModbusClient
# from pymodbus.client.sync import ModbusTcpClient as ModbusClient

# from pymodbus.transaction import ModbusSocketFramer as ModbusFramer
# from pymodbus.transaction import ModbusRtuFramer
# from pymodbus.transaction import ModbusBinaryFramer
# from pymodbus.transaction import ModbusAsciiFramer

class NativeUart(BaseProvider):
    """UART master device.
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
        self._vendor = "Native"
        self._model = "UART"

        method = self._get_option("method", "rtu")
        port = self._get_option("port")
        baudrate = self._get_option("baudrate", 9600)
        timeout = self._get_option("timeout", 1)
        bytesize = self._get_option("bytesize", 8)
        parity = self._get_option("parity", "N")
        stopbits = self._get_option("stopbits", 1)

        self.__client = ModbusClient(
                    method=method,
                    port=port,
                    baudrate=baudrate,
                    timeout=timeout,
                    bytesize=bytesize,
                    parity=parity,
                    stopbits=stopbits
                    )

#endregion

#region Private Methods

#endregion

#!/usr/bin/env python3
# -*- coding: utf8 -*-

import time

from providers.vendors.base_provider import BaseProvider

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
# from pymodbus.transaction import ModbusSocketFramer as ModbusFramer

from pymodbus.transaction import ModbusRtuFramer as ModbusFramer
# from pymodbus.transaction import ModbusBinaryFramer as ModbusFramer
# from pymodbus.transaction import ModbusAsciiFramer as ModbusFramer

class NB114(BaseProvider):
    """NB114 master device.
    """

    def __init__(self, options):
        """Constructor

        Args:
            options (dict): Options data.
        """
        super().__init__(options)
        self._vendor = "EByte"
        self._model = "NB114"

    def read_device_data(self):

        # ----------------------------------------------------------------------- #
        # Initialize the client
        # ----------------------------------------------------------------------- #

        ip = self.__get_option("ip")
        port = self.__get_option("port")

        client = ModbusClient(ip, port=port, framer=ModbusFramer)
        client.connect()

        # ----------------------------------------------------------------------- #
        # perform your requests
        # ----------------------------------------------------------------------- #
        for _ in range(0, 10):
            rq = client.write_coil(1, True)
            time.sleep(0.1)
            # rr = client.read_coils(1, 1)
            # assert not rq.isError()  # nosec test that we are not an error
            # assert rr.bits[0]  # nosec test the expected value
            rq = client.write_coil(1, False)
            time.sleep(0.1)
            # rr = client.read_coils(1, 1)
            # assert not rq.isError()  # nosec test that we are not an error
            # assert rr.bits[0]  # nosec test the expected value

        # ----------------------------------------------------------------------- #
        # close the client
        # ---------------------------------------------------------------------- #
        client.close()
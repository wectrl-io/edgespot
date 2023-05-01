#!/usr/bin/env python3
# -*- coding: utf8 -*-

import json

from utils.logger import get_logger
from devices.vendors.shelly.gen_2.gen2_device import Gen2Device

import requests

class ShellyHttpBase(Gen2Device):

#region Attributes

    __logger = None
    """Logger
    """

    _host = None
    """Host address of the device.
    """

    _port = 80
    """Port of the device.
    """

    _timeout = 1
    """Timeout
    """

    _base_url = None
    """Base URL.
    """

#endregion

#region Constructor

    def __init__(self, options, provider, adapter):
        """Constructor

        Args:
            options (dict): Instance options.
            provider (object): Data provider.
            adapter (object): Adapter collector.
        """

        super().__init__(options, provider, adapter)

        # Set logger.
        self.__logger = get_logger(__name__)

        self._host = self._get_option("host")

        self._port = self._get_option("port", 80)

        self._timeout = self._get_option("http_timeout", 1)

        self._base_url = f"http://{self._host}:{self._port}"

#endregion

#region Protected Methods

    def _get_requests(self, url):

        response = None

        try:
            response = requests.get(url, timeout=self._timeout)
            response = json.loads(response.text)

        except Exception as e:
            self.__logger.error(e)

        return response

#endregion

#region Public Method (API)

    def config(self):
        """Get configuration from the device.

        Returns:
            dict: Response from the device.
        """
        url = f"{self._base_url}/rpc/Shelly.GetConfig"
        return self._get_requests(url)

    def status(self):
        """Get status from the device.

        Returns:
            dict: Response from the device.
        """
        url = f"{self._base_url}/rpc/Shelly.GetStatus"
        return self._get_requests(url)

#endregion

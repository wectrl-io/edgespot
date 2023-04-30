#!/usr/bin/env python3
# -*- coding: utf8 -*-

from utils.logger import get_logger
from .shelly_base import ShellyBase

class Shelly1(ShellyBase):

#region Attributes

    __logger = None
    """Logger
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
        self._vendor = "Alterco"
        self._model = "Shgelly1-GEN1"

        self.__logger = get_logger(__name__)

#endregion

#region Public Methods (API)

    def relay(self, index=0, state="off"):
        """Get status from the device.

        Args:
            index (int, optional): _description_. Defaults to 0.
            state (str, optional): _description_. Defaults to "off".
        """

        url = f"{self._base_url}/relay/{index}"
        return self._get_requests(url)

#endregion
#!/usr/bin/env python3
# -*- coding: utf8 -*-

from utils.logger import get_logger
from devices.vendors.shelly.shelly_base import ShellyBase

class Gen2Device(ShellyBase):
    """Shelly devices generation 2 base class.
    """

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

        # Set logger.
        self.__logger = get_logger(__name__)

#endregion

#region Protected Methods

#endregion

#region Public Method (API)

#endregion

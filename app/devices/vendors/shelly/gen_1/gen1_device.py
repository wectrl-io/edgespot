#!/usr/bin/env python3
# -*- coding: utf8 -*-

from utils.logger import get_logger
from devices.base_device import BaseDevice

class Gen1Device(BaseDevice):
    """Shelly devices generation 1 base class.
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

#!/usr/bin/env python3
# -*- coding: utf8 -*-

from utils.logger import get_logger
from devices.vendors.shelly.shelly_base import ShellyBase

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

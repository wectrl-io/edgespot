#!/usr/bin/env python3
# -*- coding: utf8 -*-

from adapters.adapter_factory import AdaptersFactory
from devices.devices import Devices
from providers.providers_factory import ProvidersFactory
from devices.device_factory import DevicesFactory

from utils.logger import get_logger

from utils.config import AppConfig

from utils.service_locator.service_locator import ServiceLocator

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

class Edgespot(object):
    """Edgespot application logic.
    """

#region Attributes

    __logger = None
    """Logger
    """

    __service_locator = None
    """Service locator.
    """

    __settings = None
    """Application settings.
    """

    __devices = None
    """List of sub devices.
    """


#endregion

#region Constructor

    def __init__(self):
        """Constructor.
        """

        # Set logger.
        self.__logger = get_logger(__name__)

        # Get instance of the service locator.
        self.__service_locator = ServiceLocator.get_instance()

        # Get settings.
        self.__settings = AppConfig.get_instance()

        # Create and add adapters.
        adapters = self.__settings.config["adapters"]
        for adapter in adapters:
            adapter_instance = AdaptersFactory.create(adapter)
            self.__service_locator.add(adapter["name"], adapter_instance)

        # Create and add providers.
        providers = self.__settings.config["providers"]
        for provider in providers:
            provider_instance = ProvidersFactory.create(provider)
            self.__service_locator.add(provider["name"], provider_instance)

        # Create and add devices.
        self.__devices = Devices()
        devices = self.__settings.config["devices"]
        for device in devices:
            adapter = self.__service_locator.get(device["adapter"])
            provider = self.__service_locator.get(device["provider"])
            device_instance = DevicesFactory.create(device, provider, adapter)
            self.__devices.append(device_instance)

#endregion

#region Public Methods

    def init(self):
        """Initialize the edgespot.
        """

        self.__logger.info("Starting process")

        # print(f"{__name__}.{__class__}.{inspect.stack()[0][0].f_code.co_name}")
        # print(inspect.stack()[0][3])
        # print(inspect.currentframe().f_code.co_name)
        # print(sys._getframe().f_code.co_name)
        # print( )

        # Create slaves.
        for device in self.__devices:
            device.init()

    def update(self):
        """Update the edgespot.
        """

        for device in self.__devices:
            device.update()

    def shutdown(self):
        """Shutdown the edgespot.
        """

        for device in self.__devices:
            device.shutdown()

        self.__logger.info("Stopping process")

#endregion

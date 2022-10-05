#!/usr/bin/env python3
# -*- coding: utf8 -*-

from adapters.adapter_factory import AdaptersFactory
from devices.devices import Devices
from providers.providers_factory import ProvidersFactory
from devices.device_factory import DevicesFactory

from utils.logger import get_logger

from utils.settings import ApplicationSettings

class Sunspot(object):
    """Sun spot application logic.
    """

#region Attributes

    __logger = None
    """Logger
    """

    __devices = None
    """List of sub devices.
    """

    __settings = None
    """Application settings.
    """

#endregion

#region Constructor

    def __init__(self):
        """Constructor.
        """

        # Set logger.
        self.__logger = get_logger(__name__)

        # Get settings.
        self.__settings = ApplicationSettings.get_instance()

        self.__devices = Devices()
        for device_settings in self.__settings.devices:
            adapter = AdaptersFactory.create(device_settings["adapter"])
            provider = ProvidersFactory.create(device_settings["provider"])
            device = DevicesFactory.create(device_settings["device"], provider, adapter)           
            self.__devices.append(device)

#endregion

#region Public Methods

    def init(self):
        """Initialize the sunspot.
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
        """Update the sunspot.
        """

        for device in self.__devices:
            device.update()

    def shutdown(self):
        """Shutdown the sunspot.
        """

        for device in self.__devices:
            device.shutdown()

        self.__logger.info("Stopping process")

#endregion

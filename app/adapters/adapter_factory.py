#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Devices factory class.
"""

from adapters.vendors.things_board.mqtt.things_board import ThingsBoard as ThingsBoardMQTTClient
from adapters.vendors.open_remote.mqtt.open_remote import OpenRemote as OpenRemoteMQTTClient

from exceptions.unsupported_adapter import UnsupportedAdapter

class AdaptersFactory:
    """Adapters factory class.
    """

    @staticmethod
    def create(settings):
        """Create adapter.

        Args:
            settings (dict): Settings data.

        Returns:
            Any: Instance of the adapter.
        """

        instance = None

        vendor = None
        if "vendor" not in settings:
            raise ValueError("Invalid vendor")
        else:
            vendor = settings["vendor"]

        version = None
        if "version" not in settings:
            raise ValueError("Invalid model")
        else:
            version = settings["version"]

        options = None
        if "options" not in settings:
            raise ValueError("Invalid options")
        else:
            options = settings["options"]

        if vendor == "ThingsBoardMQTTClient" and version == "1.0":
            instance = ThingsBoardMQTTClient.get_instance(options)

        elif vendor == "OpenRemoteMQTTClient" and version == "1.0":
            instance = OpenRemoteMQTTClient.get_instance(options)

        else:
            raise UnsupportedAdapter(f"Unsupported adapter version({version}), vendor({vendor})")

        return instance

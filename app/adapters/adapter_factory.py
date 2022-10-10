#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Devices factory class.
"""

from adapters.vendors.thingsboard.thingsboard import ThingsBoardMQTTClient

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
            raise Exception("Invalid vendor")
        else:
            vendor = settings["vendor"]

        version = None
        if "version" not in settings:
            raise Exception("Invalid model")
        else:
            version = settings["version"]

        options = None
        if "options" not in settings:
            raise Exception("Invalid options")
        else:
            options = settings["options"]

        if vendor == "ThingsBoardMQTTClient" and version == "1.0":
            instance = ThingsBoardMQTTClient.get_instance(options)

        else:
            raise Exception(f"Unsupported adapter version({version}), vendor({vendor})")

        return instance

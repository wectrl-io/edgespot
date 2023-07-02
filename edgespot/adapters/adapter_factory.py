#!/usr/bin/env python3
# -*- coding: utf8 -*-

from edgespot.adapters.vendors.things_board.mqtt.things_board import ThingsBoard as ThingsBoardMQTTClient
from edgespot.adapters.vendors.open_remote.mqtt.open_remote import OpenRemote as OpenRemoteMQTTClient

from edgespot.exceptions.unsupported_adapter import UnsupportedAdapter

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

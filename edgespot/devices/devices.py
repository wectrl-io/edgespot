#!/usr/bin/env python3
# -*- coding: utf8 -*-

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

class Devices(list):
    """Devices list.
    """

    def by_name(self, name):
        """Get target device by name.

        Args:
            name (string): Name of the device.

        Returns:
            Any: Instance of device.
        """

        target = None

        for item in self:
            if item.name is not None or "":
                target = item

        return target

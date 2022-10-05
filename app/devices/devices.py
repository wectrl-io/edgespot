#!/usr/bin/env python3
# -*- coding: utf8 -*-

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

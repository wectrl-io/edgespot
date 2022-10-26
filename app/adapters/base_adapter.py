#!/usr/bin/env python
# -*- coding: utf8 -*-

class BaseAdapter(object):

#region Attributes

    _options = {}

#endregion

#region Constructor

    def __init__(self, options):

        self._options = options

#endregion

#region Protected Methods

    def _get_option(self, name):

        if name not in self._options:
            raise Exception(f"Invalid option: {name}")

        return self._options[name]

#endregion

#region Public Methods

    def connect(self):
        """Connect to the host.
        """

        pass

    def update(self):
        """Update the host.
        """

        pass

    def disconnect(self):
        """Disconnect from the host.
        """

        pass

    def publish(self, **kwargs):
        """Publish data to the host.
        """

        pass

    def send_telemetry(self, values, time_stamp=0):
        """Send telemetry data.

        Args:
            values (dict): Key Values dictionary.
            time_stamp (int, optional): When this data ocurred. Defaults to 0.
        """

        pass

    def send_attributes(self, values):
        """Send attributes data.

        Args:
            values (dict): Key Values dictionary.
            time_stamp (int, optional): When this data ocurred. Defaults to 0.
        """

        pass

    def subscribe(self, **kwargs):
        """Subscribe
        """

        pass

#endregion

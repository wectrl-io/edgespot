#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Base device class.
"""

class BaseDevice(object):
    """Base device class.
    """

#region Attributes

    _options = {}
    """Options
    """

    _model = "Default Model"
    _vendor = "Default Vendor"

#endregion

#region Properties

    @property
    def model(self):
        """Model

        Returns:
            string: Model
        """
        return self._model

    @property
    def vendor(self):
        """Vendor

        Returns:
            string: Vendor
        """
        return self._vendor

    @property
    def name(self):
        """Returns device name.

        Returns:
            str: Device name.
        """

        return self._get_option("name")

    def __str__(self):
        name = self._get_option("name")
        return f"name({name})/vendor({self.vendor})/model({self.model})"

    __repr__ = __str__

#endregion

#region Constructor

    def __init__(self, options, provider, adapter):
        """Constructor

        Args:
            options (dict): Instance options.
            provider (object): Data provider.
            adapter (object): Adapter collector.

        Raises:
            ValueError: _description_
        """
        if options is None:
            raise ValueError("Invalid options")

        self._options = options
        self._provider = provider
        self._adapter = adapter

#endregion

#region Protected Methods

    def _get_option(self, name, default=None):
        """Get option from options.

        Args:
            name (str): Option name.
            default (any, optional): Default value if there any. Defaults to None.

        Raises:
            ValueError: Invalid option name.

        Returns:
            str: option value.
        """

        if name not in self._options and default is None:
            raise ValueError(f"Invalid option: {name}")

        if name not in self._options and default is not None:
            return default

        return self._options[name]

#endregion

#region Public Methods

    def init(self):

        pass
    
    def update(self):

        pass
    
    def shutdown(self):

        pass

#endregion

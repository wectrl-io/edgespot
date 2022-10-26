#!/usr/bin/env python3
# -*- coding: utf8 -*-

from providers.vendors.base_provider import BaseProvider

class Dummy(BaseProvider):
    """Dummy Provider
    """

    def __init__(self, options):
        """Constructor

        Args:
            options (dict): Options data.
        """

        super().__init__(options)
        self._vendor = "Dummy"
        self._model = "Dummy"

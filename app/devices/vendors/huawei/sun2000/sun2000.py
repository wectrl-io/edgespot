#!/usr/bin/env python3
# -*- coding: utf8 -*-

#!/usr/bin/env python3
# -*- coding: utf8 -*-

import random
from devices.base_device import BaseDevice
from utils.timer import Timer
from utils.logger import get_logger

class SUN2000(BaseDevice):
    """Huawei SUN2000 device.
    """

#region Attributes

    __logger = None
    """Logger
    """

#endregion

#region Constructor

    def __init__(self, options, provider, adapter):
        """Constructor

        Args:
            options (dict): Options data.
        """

        super().__init__(options, provider, adapter)
        self._vendor = "Huawei"
        self._model = "SUN2000"

        # Set logger.
        self.__logger = get_logger(__name__)

#endregion

#region Public Methods

    def init(self):

        self._adapter.connect()

    def update(self):

        self._adapter.update()

    def shutdown(self):

        pass

#endregion

#region Private Methods

#endregion

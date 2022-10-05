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

    __logger = None
    """Logger
    """

    __timer = None
    """Update timer.
    """

    __update_period = 1
    """Update period.
    """

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

        # Set timer.
        self.__timer = Timer(self.__update_period)
        self.__timer.set_callback(self.__timer_cb)

    def __get_params(self):

        return {"value1": random.randint(0, 9), "value2": random.randint(0, 9)}

#region Public Methods

    def init(self):

        self._adapter.connect()

    def update(self):

        self.__timer.update()
        self._adapter.update()

    def shutdown(self):

        pass

#endregion

#region Private Methods

    def __timer_cb(self, timer):

        timer.clear()

        params = self.__get_params()

        data = self._provider.get_data(params)

        self._adapter.send_telemetry(data)

        # self.__logger.info("Working process")

#endregion

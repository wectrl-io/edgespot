#!/usr/bin/env python3
# -*- coding: utf8 -*-

from enum import Enum

class GWTypes(Enum):
    """Supproted Gateway Types
    """

    NONE = 0
    SERIAL_RTU = 1
    SERIAL_ASCII = 2
    TCP_RTU = 3
    TCP_ASCII = 4
    UDP_RTU = 5
    UDP_ASCII = 6
    TCP_RTU_FRAMER = 7

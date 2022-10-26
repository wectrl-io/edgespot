#!/usr/bin/env python3
# -*- coding: utf8 -*-

class UnitOfMeasurement(Exception):
    pass

class MissingParameter(Exception):
    pass

class InvalidOption(Exception):
    pass

class UnsuportedFramer(Exception):
    pass

class UnsuportedAdapter(Exception):
    pass

class UnsuportedDevice(Exception):
    pass

class UnsupportedProvider(Exception):
    pass

class InvalidAtribute(Exception):
    pass

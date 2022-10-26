#!/usr/bin/env python3
# -*- coding: utf8 -*-

from exceptions.exceptions import InvalidAtribute
from exceptions.exceptions import UnitOfMeasurement


def get_value_from_entity(state):

    value = None

    if state.attributes["unit_of_measurement"] is None:
        raise InvalidAtribute("Unt of measurement is None.")

    if state.attributes["unit_of_measurement"] == "kWh":
        value = float(state.state)

    else:
        raise UnitOfMeasurement("Unknown unit of measurement.")

    return value

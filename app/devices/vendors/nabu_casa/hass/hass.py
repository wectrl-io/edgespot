#!/usr/bin/env python3
# -*- coding: utf8 -*-

import json
import random
import time

from devices.base_device import BaseDevice
from utils.timer import Timer
from utils.logger import get_logger

from hassapi import Hass

class HomeAssistant(BaseDevice):
    """HomeAssistant"""

#region Attributes

    __logger = None
    """Logger
    """

    __hass = None
    """Hass instance.
    """

    __update_period = 1

    __states_ids = []

#endregion

#region Constructor

    def __init__(self, options, provider, adapter):
        """Constructor

        Args:
            options (dict): Options data.
        """

        super().__init__(options, provider, adapter)
        self._vendor = "nabu_casa"
        self._model = "hass"

        # Set logger.
        self.__logger = get_logger(__name__)

        # Set home assistant.
        hassurl = self._get_option("hassurl")
        token = self._get_option("token")
        self.__hass = Hass(hassurl=hassurl, token=token)

        # Update period of the pooling cycle.
        self.__update_period = self._get_option("update_period", 1)
        self.__timer = Timer(self.__update_period)
        self.__timer.set_callback(self.__timer_cb)

        # Get states IDs.
        self.__states_ids = self._get_option("states_ids", [])

#endregion

#region Private Methods

    def __timer_cb(self, timer):

        # Clear the timer.
        timer.clear()

        parameters = []

        for entity_id in self.__states_ids:
            state = self.__hass.get_state(entity_id)
            print(entity_id)
            print(state)
            parameters[entity_id] = state

        # self.__hass.turn_on("light.bedroom_light")
        # self.__hass.run_script("good_morning")

        # Send data to the cloud.
        # self._adapter.send_telemetry(parameters)

    def __get_gpio_status(self):

        return json.dumps(self.__gpio_state)

    def __set_gpio_status(self, pin, status):

        # Update GPIOs state.
        self.__gpio_state[pin] = status

    def __on_message(self, client, userdata, message):

        # Log message.
        self.__logger.info(\
            f"Topic: {message.topic}; Message: {message.payload}")

        # Decode JSON request
        data = json.loads(message.payload)

        # Check request method
        if data['method'] == 'getGpioStatus':
            # Reply with GPIO status.
            client.publish(message.topic.replace('request', 'response'), self.__get_gpio_status(), 1)

        elif data['method'] == 'setGpioStatus':
            # Update GPIO status and reply.
            self.__set_gpio_status(data['params']['pin'], data['params']['enabled'])
            client.publish(message.topic.replace('request', 'response'), self.__get_gpio_status(), 1)
            client.publish('v1/devices/me/attributes', self.__get_gpio_status(), 1)

            self.__update_do_ro()

    def __update_do_ro(self):
        states = []
        for gpio, state in self.__gpio_state.items():
            states.append(state)

        client = self._provider.communicator
        unit = self._get_option("modbus_id")
        client.connect()
        client.write_coils(0, states, unit=unit)
        client.close()
            

#endregion

#region Public Methods

    def init(self):

        self._adapter.connect()
        self._adapter.subscribe(gpio_state=self.__get_gpio_status, callback=self.__on_message)

    def update(self):

        self.__timer.update()
        self._adapter.update()

    def shutdown(self):

        self._adapter.disconnect()

#endregion

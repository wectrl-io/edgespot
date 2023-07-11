#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
import time

import paho.mqtt.client as mqtt

from adapters.base_adapter import BaseAdapter
from utils.logger import get_logger

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = ""
"""Copyrighted"""

__credits__ = []
"""Credits"""

__license__ = ""
"""License
@see """

__version__ = "1.0.0"
"""Version of the file."""

__maintainer__ = ["Orlin Dimitrov", "Martin Maslyankov", "Nikola Atanasov"]
"""Name of the maintainer."""

__email__ = ""
"""E-mail of the author."""

__class_name__ = ""
"""Class name."""

#endregion

class ThingsBoard(BaseAdapter):
    """Things Board MQTT client.
    """

#region Attributes

    __logger = None
    """Logger
    """

    __mqtt_client = None
    """MQTT client.
    """

    __host = "127.0.0.1"
    """Host of the broker.
    """

    __port= 1883
    """Port of the broker service.
    """

    __keep_alive = 60
    """Keep alive time.
    """

    __token = ""
    """Communication token.
    """

    __cb = None
    """Event handle.
    """

#endregion

#region Constructor

    def __init__(self, options):
        super().__init__(options)

        # Create logger.
        self.__logger = get_logger(__name__)

        # Get host name to the cloud.
        self.__host = self._get_option("host")

        # Get port to the cloud.
        port = self._get_option("port")
        if 1 < port > 65535 :
            raise ValueError(f"Invalid parameter port = {port}")
        self.__port = port

        # Get keep alive time to the cloud.
        keep_alive = self._get_option("keep_alive")
        if 1 < keep_alive > 3600 :
            raise ValueError(f"Invalid parameter keep_alive = {keep_alive}")
        self.__keep_alive = keep_alive

        # Get token data.
        self.__token = self._get_option("token")

        # Create
        self.__mqtt_client = mqtt.Client(client_id="", clean_session=True)
        self.__mqtt_client.on_publish = self.__on_publish
        self.__mqtt_client.on_message = self.__on_message
        self.__mqtt_client.on_connect = self.__on_connect
        self.__mqtt_client.on_subscribe = self.__on_subscribe
        self.__mqtt_client.on_disconnect = self.__on_disconnect
        self.__mqtt_client.username_pw_set(self.__token)

#endregion

#region Public Methods

    def connect(self):
        """Connect to MQTT broker.
        """

        if self.__mqtt_client is None:
            raise ValueError("Invalid MQTT client instance.")

        # Connect to the broker.
        self.__mqtt_client.connect(host=self.__host, port=self.__port, keepalive=self.__keep_alive)

        # Subscribing to receive RPC requests
        self.__mqtt_client.subscribe('v1/devices/me/rpc/request/+')

    def update(self):
        """Update the MQTT client.

        Raises:
            Exception: _description_
        """

        if self.__mqtt_client is None:
            raise ValueError("Invalid MQTT client instance.")

        # Continue monitoring the incoming messages for subscribed topic.
        self.__mqtt_client.loop()

    def disconnect(self):
        """Disconnect from MQTT broker.

        Raises:
            Exception: _description_
        """

        if self.__mqtt_client is None:
            raise ValueError("Invalid MQTT client instance.")

        self.__mqtt_client.disconnect()

    def publish(self, topic, message):
        """Publish data.

        Args:
            topic (string): Topic
            message (Bytes): Message

        Raises:
            Exception: Invalid MQTT client instance.
        """

        if self.__mqtt_client is None:
            raise ValueError("Invalid MQTT client instance.")

        self.__mqtt_client.publish(topic, message)

    def send_telemetry(self, values, time_stamp=0):
        """Send telemetry data.

        Args:
            values (dict): Key Values dictionary.
            time_stamp (int, optional): When this data ocurred. Defaults to 0.
        """

        if self.__mqtt_client is None:
            raise ValueError("Invalid MQTT client instance.")

        # Constancy check the timestamp.
        if time_stamp <= 0:
            time_stamp = time.time()

        # Shift to [ms] band.
        time_stamp *= 1000

        # Make it integer.
        time_stamp = int(time_stamp)

        # Create message.
        values = {'ts' : time_stamp, 'values' : values}
        values = json.dumps(values)

        # Send message.
        # Topic: v1/devices/me/telemetry
        self.__mqtt_client.publish("v1/devices/me/telemetry", values)

    def subscribe(self, **kwargs):
        """Subscribe
        """

        if "callback" in kwargs and kwargs["callback"] is not None:
            self.__cb = kwargs["callback"]

        if "gpio_state" in kwargs and kwargs["gpio_state"] is not None:
            gpio_state = kwargs["gpio_state"]
            values = gpio_state()
            self.__mqtt_client.publish("v1/devices/me/attributes", values)

#endregion

#region Private Methods

    def __on_publish(self, client, userdata, result):

        # self.__logger.debug(\
        #     f"Publish to {self.__host} from {client} with {userdata}: result {result}")

        pass

    def __on_message(self, client, userdata, message):

        if self.__cb is not None:
            self.__cb(client, userdata, message)

    def __on_connect(self, client, userdata, flags, rc):

        if rc==0:
            self.__logger.info(f"Connected OK Returned code {rc}")

        else:
            self.__logger.error(f"Bad connection Returned code {rc}")

    def __on_subscribe(self, client, userdata, mid, rc):

        self.__logger.info(\
            f"Subscribe to {self.__host}; rc {rc}")

    def __on_disconnect(self, client, userdata, rc):

        self.__logger.info(\
            f"Disconnect {self.__host}; rc {rc}")

#endregion

#region Static Methods

    @staticmethod
    def get_instance(options):
        """Get instance of the Thinks Board MQTT Client.

        Args:
            settings (dict): Settings dictionary.
        """

        if "host" not in options:
            raise ValueError("No host provided.")

        if "port" not in options:
            raise ValueError("No port provided.")

        if "token" not in options:
            raise ValueError("No token provided.")

        return ThingsBoard(options)

#endregion

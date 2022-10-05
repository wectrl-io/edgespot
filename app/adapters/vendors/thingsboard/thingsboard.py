#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
import time

from utils.logger import get_logger

import paho.mqtt.client as mqtt

class ThingsBoardMQTTClient(object):
    """Things Board MQTT client.
    """

#region Attributes

    __logger = None
    """Logger
    """

    __mqtt_client = None
    """MQTT client.
    """

    __host = "devcloud.dreamtomation.com"
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

    __cid = ""
    """Client ID
    """

#endregion

#region Constructor

    def __init__(self, host, port=1883, keep_alive=60, **kwargs):

        if host is None:
            raise Exception(f"Invalid parameter host = {host}")
        self.__host = host

        if 1 < port > 65535 :
            raise Exception(f"Invalid parameter port = {port}")
        self.__port = port

        if 1 < keep_alive > 3600 :
            raise Exception(f"Invalid parameter keep_alive = {keep_alive}")
        self.__keep_alive = keep_alive

        # Get token data.
        if "token" in kwargs:

            if kwargs["token"] is None:
                raise Exception("Invalid token")

            self.__token = kwargs["token"]

        # Get client ID.
        if "cid" in kwargs:

            if kwargs["cid"] is None:
                raise Exception("Invalid token")

            self.__cid = kwargs["cid"]

        # Create logger.
        self.__logger = get_logger(__name__)

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
            raise Exception("Invalid MQTT client instance.")

        # Connect to the broker.
        self.__mqtt_client.connect(host=self.__host, port=self.__port, keepalive=self.__keep_alive)

        # Subscribe to the attributes.
        self.__mqtt_client.subscribe("v1/devices/me/attributes", 0)

    def update(self):
        """Update the MQTT client.

        Raises:
            Exception: _description_
        """

        if self.__mqtt_client is None:
            raise Exception("Invalid MQTT client instance.")

        # Continue monitoring the incoming messages for subscribed topic.
        self.__mqtt_client.loop()

    def disconnect(self):
        """Disconnect from MQTT broker.

        Raises:
            Exception: _description_
        """

        if self.__mqtt_client is None:
            raise Exception("Invalid MQTT client instance.")

        self.__mqtt_client.disconnect()

    def send_telemetry(self, values, time_stamp=0):
        """Send telemetry data.

        Args:
            parameters_values (_type_): _description_
            time_stamp (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: _description_
        """

        if self.__mqtt_client is None:
            raise Exception("Invalid MQTT client instance.")

        # Constancy check the timestamp.
        if time_stamp <= 0:
            time_stamp = time.time()

        # Shift to [ms] band.
        time_stamp *= 1000

        values = {'ts' : time_stamp, 'values' : values}
        values = json.dumps(values)
        self.__mqtt_client.publish("v1/devices/me/telemetry", values) #topic-v1/devices/me/telemetry

#endregion

#region Private Methods

    def __on_publish(self, client, userdata, result):

        # self.__logger.info(\
        #     f"__on_publish {self.__host} from {client} with {userdata}: result {result}")

        pass

    def __on_message(self, client, userdata, result):

        self.__logger.info(\
            f"__on_message {self.__host} from {client} with {userdata}: result {result}")

    def __on_connect(self, client, userdata, flags, rc):

        if rc==0:
            self.__logger.info(f"Connected OK Returned code {rc}")

        else:
            self.__logger.error(f"Bad connection Returned code {rc}")

    def __on_subscribe(self, client, userdata, mid, rc):

        self.__logger.info(\
            f"__on_subscribe {self.__host} from {client} with {userdata}: rc {rc}")

    def __on_disconnect(self, client, userdata, rc):

        self.__logger.info(\
            f"__on_disconnect {self.__host} @ {client} with {userdata}: rc {rc}")

#endregion

#region Static Methods

    @staticmethod
    def get_instance(settings):
        """Get instance of the Thinks Board MQTT Client.

        Args:
            settings (dict): Settings dictionary.
        """

        if "host" not in settings:
            raise Exception("No host provided.")

        if "port" not in settings:
            raise Exception("No port provided.")

        if "token" not in settings:
            raise Exception("No token provided.")

        host = settings["host"]
        port = settings["port"]
        token = settings["token"]

        # client.connect()
        # client.update()
        # client.send_telemetry({"value": random.randint(0, 9)})

        return ThingsBoardMQTTClient(host, port, token=token)

#endregion

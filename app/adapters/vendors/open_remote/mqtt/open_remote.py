#!/usr/bin/env python
# -*- coding: utf8 -*-

from adapters.base_adapter import BaseAdapter
from utils.logger import get_logger

import paho.mqtt.client as mqtt

class OpenRemote(BaseAdapter):
    """Open Remote MQTT client.
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

    __client_id = ""
    """Communication token.
    """

    __cb_dispatcher = {}
    """Callback dispatcher.
    """

    __is_connected_flag = False
    """Is connected flag.
    """    

#endregion

#region Properties

    @property
    def is_connected(self):
        """Is connected flag.

        Returns:
            bool: Is connected flag.
        """

        return self.__is_connected_flag

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
        client_id = self._get_option("client_id")
        if client_id == "":
            raise ValueError(f"Invalid parameter client_id = {client_id}")
        self.__client_id = client_id

        # Create the MQTT client.
        self.__mqtt_client = mqtt.Client(client_id=self.__client_id, clean_session=True)
        self.__mqtt_client.on_publish = self.__on_publish
        self.__mqtt_client.on_message = self.__on_message
        self.__mqtt_client.on_connect = self.__on_connect
        self.__mqtt_client.on_subscribe = self.__on_subscribe
        self.__mqtt_client.on_disconnect = self.__on_disconnect
        self.__mqtt_client.username_pw_set(self.__client_id)

#endregion

#region Private Methods (API)

    def __attach_cb_to_topic(self, topic, callback):

        if self.__cb_dispatcher is not []:
            self.__cb_dispatcher[topic] = []

        if topic in self.__cb_dispatcher:
            if self.__cb_dispatcher[topic] is []:
                self.__cb_dispatcher[topic].append(callback)

    def __dispatch_message(self, client, userdata, message):

        if message is None:
            return

        if message.topic is None:
            return

        for topic in self.__cb_dispatcher:
            if topic == message.topic:
                if callable(self.__cb_dispatcher[message.topic]):
                    self.__cb_dispatcher[message.topic](client, userdata, message)

#endregion

#region Private Methods (MQTT)

    def __on_publish(self, client, userdata, result):

        self.__logger.debug(\
            f"Publish to {self.__host} from {client} with {userdata}: result {result}")

    def __on_message(self, client, userdata, message):

        self.__dispatch_message(client, userdata, message)

    def __on_connect(self, client, userdata, flags, rc):

        if rc == 0:
            self.__logger.info(f"Connected OK Returned code {rc}")
            self.__is_connected_flag = True

        else:
            self.__logger.error(f"Bad connection Returned code {rc}")
            self.__is_connected_flag = False

    def __on_subscribe(self, client, userdata, mid, rc):

        self.__logger.info(\
            f"Subscribe to {self.__host}; rc {rc}")

    def __on_disconnect(self, client, userdata, rc):

        self.__logger.info(\
            f"Disconnect from {self.__host}, with return code {rc}")
        self.__is_connected_flag = False

#endregion

#region Public Methods (API)

    def pub_attribute(self, realm_name: str, attribute_name: str, asset_id: str, value):
        """Publish to attribute.

        Args:
            realm_name (str): Realm name.
            attribute_name (str): Attribute name.
            asset_id (str): Asset ID.
            callback (function): Callback function

        Raises:
            ValueError: Invalid MQTT client.
        """

        if self.__mqtt_client is None:
            raise ValueError("Invalid MQTT client instance.")

        if not self.is_connected:
            return

        # Create topic to write to attribute value.
        #          master     /client123         /writeattributevalue/writeAttribute  /6xIa9MkpZuR7slaUGB6OTZ
        topic = f"{realm_name}/{self.__client_id}/writeattributevalue/{attribute_name}/{asset_id}"

        # Send message.
        self.__mqtt_client.publish(topic, value)

    def sub_attribute(self, realm_name: str, attribute_name: str, asset_id: str, callback):
        """Subscribe to attribute.

        Args:
            realm_name (str): Realm name.
            attribute_name (str): Attribute name.
            asset_id (str): Asset ID.
            callback (function): Callback function

        Raises:
            ValueError: Invalid MQTT client.
        """

        # Create topic to write to attribute value.
        #          master     /client123         /attribute/subscribeAttribute/6xIa9MkpZuR7slaUGB6OTZ
        topic = f"{realm_name}/{self.__client_id}/attribute/{attribute_name}/{asset_id}"

        self.__attach_cb_to_topic(topic, callback)

        if self.__mqtt_client is None:
            raise ValueError("Invalid MQTT client instance.")

        if not self.is_connected:
            return

        # Subscribing to receive RPC requests.
        self.__mqtt_client.subscribe(topic)

#endregion

#region Public Methods (Base Class Implementation)

    def connect(self):
        """Connect to MQTT broker.
        """

        if self.__mqtt_client is None:
            raise ValueError("Invalid MQTT client instance.")

        if self.is_connected:
            return

        # Connect to the broker.
        self.__mqtt_client.connect(host=self.__host, port=self.__port, keepalive=self.__keep_alive)
        self.__mqtt_client.loop()

    def update(self):
        """Update the MQTT client.

        Raises:
            Exception: _description_
        """

        if self.__mqtt_client is None:
            raise ValueError("Invalid MQTT client instance.")

        if not self.is_connected:
            return

        # Continue monitoring the incoming messages for subscribed topic.
        self.__mqtt_client.loop()

    def disconnect(self):
        """Disconnect from MQTT broker.

        Raises:
            Exception: _description_
        """

        if self.__mqtt_client is None:
            raise ValueError("Invalid MQTT client instance.")

        if not self.is_connected:
            return

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

        if not self.is_connected:
            return

        self.__mqtt_client.publish(topic, message)

#endregion

#region Static Methods

    @staticmethod
    def get_instance(options):
        """Get instance of the Open Remote MQTT Client.

        Args:
            settings (dict): Settings dictionary.
        """

        if "host" not in options:
            raise ValueError("No host provided.")

        if "port" not in options:
            raise ValueError("No port provided.")

        if "client_id" not in options:
            raise ValueError("No client ID provided.")

        return OpenRemote(options)

#endregion

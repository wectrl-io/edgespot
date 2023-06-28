#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os

import yaml

from edgespot.utils.yaml_loader import Loader

class AppConfig:
    """Application configuration class."""

#region Attributes

    __file_name = ""
    """File name"""

    __instance = None
    """Singleton instance object."""

    __config = {}
    """Actual settings."""

#endregion

#region Properties

    @property
    def exists(self):
        """Does the the settings file exists.
        Returns
        -------
        bool
            File exists.
        """

        return os.path.exists(self.__file_name)

    @property
    def debug_level(self):
        """Debug level.
        Returns
        -------
        int
            Debug level.
        """

        value = None

        if self.__config is not None:
            if "application" in self.__config:
                value = self.__config["application"]["debug_level"]

        if value is None:
            value = 10

        value = int(value)

        return value

    @property
    def config(self):
        """Endpoints settings.

        Returns:
            dict: Application configuration.
        """

        return self.__config

    @property
    def path(self):
        """File name with settings.
        """

        return self.__file_name

#endregion

#region Constructor

    def __init__(self, file_name=None):
        """Constructor
        Parameters
        ----------
        file_name : str
            File name.
        """

        if AppConfig.__instance is not None:
            raise Exception("This class is a singleton!")

        AppConfig.__instance = self

        self.__file_name = ""

        if file_name is None:

            # Current file path. & Go to file.
            cwf = os.path.dirname(os.path.abspath(__file__))
            self.__file_name = os.path.join(cwf, "..", "config.yaml")

        else:
            self.__file_name = file_name

        self.load()

#endregion

#region Public Methods

    def load(self):
        """Read YAML file."""

        if self.exists:
            with open(self.__file_name, "rt", encoding="utf-8") as stream:
                self.__config = yaml.load(stream, Loader=Loader)
                stream.close()

    def save(self):
        """Read YAML file."""

        with open(self.__file_name, "wt", encoding="utf-8") as stream:
            yaml.dump(self.__config, stream)
            stream.close()

    def create_default(self):
        """Create default settings.
        """

        # Clear the config and new.
        self.__config = {}

        if self.__config is not None:
            # Default debug level.
            if "application" not in self.__config:
                self.__config["application"] = {"debug_level": 10}

            # Default masters
            if "adapters" not in self.__config:
                self.__config["adapters"] = [
                    {
                        "name": "mqtt_or",
                        "vendor": "OpenRemoteMQTTClient",
                        "version": "1.0",
                        "options":
                        {
                            "host": "home.iot.loc",
                            "port": 1883,
                            "client_id": "A1_TEST_TOKEN",
                            "keep_alive": 1,
                        }
                    }
                ]


            # Default things board credentials.
            if "devices" not in self.__config:
                self.__config["devices"] = [
                    {
                        "name": "DummyDevice1",
                        "model": "dummy",
                        "vendor": "dummy",
                        "adapter": "mqtt_or",
                        "provider": "dummy",
                        "options": {
                            "no": "no"
                        }
                    },
                    {
                        "name": "LivinroomLamp",
                        "model": "shelly_1l_gen1",
                        "vendor": "alterco",
                        "adapter": "mqtt_or",
                        "provider": "dummy",
                        "options": {
                            "host": "172.33.1.233",
                            "port": 80,
                            "update_period": 5
                        }
                    },
                    {
                        "name": "PowerMeter",
                        "model": "shelly_3em_gen1",
                        "vendor": "alterco",
                        "adapter": "mqtt_or",
                        "provider": "dummy",
                        "options": {
                            "host": "172.33.1.224",
                            "port": 80,
                            "update_period": 5
                        }
                    },
                    {
                        "name": "BathLamps",
                        "model": "shelly_2p5_gen1",
                        "vendor": "alterco",
                        "adapter": "mqtt_or",
                        "provider": "dummy",
                        "options": {
                            "host": "172.33.1.229",
                            "port": 80,
                            "update_period": 5
                        }
                    },
                    {
                        "name": "BathFan",
                        "model": "shelly_plus_1_gen2",
                        "vendor": "alterco",
                        "adapter": "mqtt_or",
                        "provider": "dummy",
                        "options": {
                            "host": "172.33.1.226",
                            "port": 80,
                            "update_period": 5
                        }
                    },
                    {
                        "name": "TS",
                        "model": "xy-md02",
                        "vendor": "donkger",
                        "adapter": "mqtt_or",
                        "provider": "white_gw",
                        "options": {
                            "modbus_id": 5,
                            "update_period": 10
                        }
                    }
                ]
            # Default slaves
            if "providers" not in self.__config:
                self.__config["providers"] = [
                    {
                        "name": "black_gw",
                        "model": "nb114",
                        "vendor": "ebyte",
                        "options": {
                            "ip": "172.33.1.33",
                            "port": 8887,
                            "framer_type": "rtu"
                        }
                    },
                    {
                        "name": "white_gw",
                        "model": "5143d",
                        "vendor": "zlan",
                        "options": {
                            "ip": "10.1.1.34",
                            "port": 4196,
                            "framer_type": "rtu"
                        }
                    },
                    {
                        "name": "white_gw_old",
                        "model": "5143d",
                        "vendor": "zlan",
                        "options": {
                            "ip": "172.33.4.124",
                            "port": 4196,
                            "framer_type": "rtu"
                       }
                    },
                    {
                        "name": "dummy",
                        "model": "dummy",
                        "vendor": "dummy",
                        "options": {
                            "no": "no"
                        }
                    }
                ]

        self.save()

#endregion

#region Static Methods

    @staticmethod
    def get_instance(file_path=None):
        """Singelton instance."""

        if AppConfig.__instance is None:
            AppConfig(file_path)

        return AppConfig.__instance

#endregion

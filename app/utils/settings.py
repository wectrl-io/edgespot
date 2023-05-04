#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os

import yaml

from utils.yaml_loader import Loader

class ApplicationSettings:
    """Application settings class."""

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

        if ApplicationSettings.__instance is not None:
            raise Exception("This class is a singleton!")

        ApplicationSettings.__instance = self

        self.__file_name = ""

        if file_name is None:

            # Current file path. & Go to file.
            cwf = os.path.dirname(os.path.abspath(__file__))
            self.__file_name = os.path.join(cwf, "..", "settings.yaml")

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

            # Default things board credentials.
            if "broker" not in self.__config:
                self.__config["broker"] = {
                    "host": "127.0.0.1",
                    "port": 1883,
                    "token": "A1_TEST_TOKEN",
                }

            # Default masters
            if "masters" not in self.__config:
                self.__config["masters"] = [
                        {
                            "vendor": "ebyte",
                            "model": "nb114",
                            "options": {"name": "Master1", "ip": "172.33.1.33", "port": 8887}
                        },
                        {
                            "vendor": "ebyte",
                            "model": "nb114",
                            "options": {"name": "Master2", "ip": "172.33.1.33", "port": 8887}
                        },
                    ]

            # Default slaves
            if "slaves" not in self.__config:
                self.__config["slaves"] = [
                        {
                            "vendor": "huawei",
                            "model": "sun2000",
                            "options": {"name": "Inverter 1", "modbus_id": 1, "master": "Master1"}
                        },
                        {
                            "vendor": "huawei",
                            "model": "sun2000",
                            "options": {"name": "Inverter 2", "modbus_id": 2, "master": "Master1"}
                        },
                        {
                            "vendor": "huawei",
                            "model": "sun2000",
                            "options": {"name": "Inverter 3", "modbus_id": 3, "master": "Master1"}
                        }
                    ]

        self.save()

#endregion

#region Static Methods

    @staticmethod
    def get_instance(file_path=None):
        """Singelton instance."""

        if ApplicationSettings.__instance is None:
            ApplicationSettings(file_path)

        return ApplicationSettings.__instance

#endregion

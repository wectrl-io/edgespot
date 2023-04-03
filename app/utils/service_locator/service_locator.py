#!/usr/bin/env python3
# -*- coding: utf8 -*-

from exceptions.invalid_service_name import InvalidServiceName
from exceptions.invalid_service_instance import InvalidServiceInstance
from exceptions.existing_service_name import ExistingServiceName
from exceptions.existing_service_instance import ExistingServiceInstance
from exceptions.not_existing_service import NotExistingService


class ServiceLocator():
    """Service locator implementation.
    """

#region Attributes

    __instance = None

    __services = {}

#endregion

#region Properties

    @property
    def names(self):
        names = []

        for service in self.__services:
            names.append(service)

        return names

#endregion

#region Constructor

    def __init__(self):
        pass

#endregion

#region Public Methods

    def add(self, name: str, service):
        """Adds the service to list of services.

        Args:
            name (str): Unique name of the service.
            service (object): Instance of the service.

        Raises:
            InvalidServiceName: Service name should be unique and not empty string.
            ExistingServiceName: Service name already exists.
            InvalidServiceInstance: Service should not be instance of None.
            ExistingServiceInstance: Service instance already exists.
        """

        if name == "":
            raise InvalidServiceName("Service name should be unique and not empty string.")

        if name in self.__services:
            raise ExistingServiceName("Service name already exists.")

        if service is None:
            raise InvalidServiceInstance("Service should not be instance of None.")

        for service_name in self.__services:
            if self.__services[service_name] == service:
                raise ExistingServiceInstance("Service instance already exists.")

        self.__services[name] = service

    def get(self, name: str) -> object:
        """Returns the service name.

        Args:
            name (str): Existing name of the service.

        Raises:
            InvalidServiceName: Service name should be unique and not empty string.
            NotExistingService: Service does not exists.

        Returns:
            object: Instance of the service.
        """

        if name == "":
            raise InvalidServiceName("Service name should be unique and not empty string.")

        if name not in self.__services:
            raise NotExistingService("Service does not exists.")

        return self.__services[name]

#endregion

#region Public Static Methods

    @staticmethod
    def get_instance():
        """Returns instance of the service locator.

        Returns:
            ServiceLocator: The instance of service locator
        """

        if ServiceLocator.__instance is None:
            ServiceLocator.__instance = ServiceLocator()

        return ServiceLocator.__instance

#endregion

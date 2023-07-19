#!/usr/bin/env python3
# -*- coding: utf8 -*-

import time

class Timer:
    """Timer class."""

#region Attributes

    __expired = False
    """Expired flag."""

    __expiration_time = 0
    """Expiration time."""

    __last_time = 0
    """Last time."""

    __now = 0
    """Current time."""

    __callback = None
    """Callback when expire."""

#endregion

#region Constructor

    def __init__(self, expiration_time=None):
        """Constructor

        Parameters
        ----------
        self : Template
            Current class instance.
        """

        if expiration_time is not None:
            self.expiration_time = expiration_time

#endregion

#region Properties

    @property
    def now(self):
        """Now time.

        Returns
        -------
        float
            Current time of the timer.
        """

        return self.__now

    @property
    def expired(self):
        """Expired flag.

        Returns
        -------
        bool
            expired flag.
        """

        return self.__expired

    @property
    def expiration_time(self):
        """Get expiration time in seconds.

        Returns
        -------
        float
            Expiration time.
        """

        return self.__expiration_time

    @expiration_time.setter
    def expiration_time(self, value):
        """Set expiration time in seconds.

        Parameters
        ----------
        value : value
            Expiration time in seconds.
        """

        self.__expiration_time = value

#endregion

#region Public Methods

    def update_last_time(self, value=None):
        """Update last time.

        Parameters
        ----------
        value : value
            Last update in time.
        """

        if value is None:
            self.__last_time = time.time()
        else:
            self.__last_time = value

    await def update(self):
        """Update cycle of the timer."""

        # Recalculate passed time.
        self.__now = time.time()
        pass_time = self.__now - self.__last_time
        if pass_time >= self.__expiration_time:
            self.__expired = True

            # Execute if there is callback attached.
            if self.__callback is not None:
                self.__callback(self)

            # Update current time.
            self.__last_time = time.time()

    def clear(self):
        """Clear"""

        if self.__expired:
            self.__expired = False

    def set_callback(self, value):
        """Set callback.

        Parameters
        ----------
        value : value
            Expiration time in seconds.
        """

        self.__callback = value

#endregion

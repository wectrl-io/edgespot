#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import logging
from time import gmtime, strftime

from edgespot.utils.config import AppConfig

#region Variables

__MODULES_NAMES = []
"""Modules names."""

#endregion

#region Public Functions

def crate_log_file(logs_dir_name="logs"):
    """This method create a new instance of the LOG directory.
    Parameters
    ----------
    logs_dir_name : str
        Path to the log directory.
    """

    settings = AppConfig.get_instance()
    debug_level = settings.debug_level
    full_dir_path = "/"

    # Current file path. & Go to file.
    cwf = os.path.dirname(os.path.abspath(__file__))
    full_dir_path = os.path.join(cwf, "..", logs_dir_name)

    # Crete log directory.
    if not os.path.exists(full_dir_path):
        os.makedirs(full_dir_path)

    # File name.
    log_file = strftime("%Y%m%d", gmtime()) + ".log"
    log_file = os.path.join(full_dir_path, log_file)

    # create message format.
    log_format = "%(asctime)s\t%(levelname)s\t%(name)s\t:%(lineno)s\t%(message)s"

    # Set basic config.
    logging.basicConfig(
        filename=log_file,
        level=debug_level,
        format=log_format)

def get_logger(module_name):
    """Get logger instance.
    Parameters
    ----------
    module_name : str
        Logger module name.
    Returns
    -------
    logger
        Logger instance.
    """

    global __MODULES_NAMES

    logger = logging.getLogger(module_name)

    if module_name in __MODULES_NAMES:
        return logger

    __MODULES_NAMES.append(module_name)

    # Get debug level.
    debug_level = AppConfig.get_instance().debug_level

    # Create console handler.
    console_handler = logging.StreamHandler()

    # Set debug level.
    console_handler.setLevel(debug_level)

    # Add console handler to logger.
    logger.addHandler(console_handler)

    return logger

#endregion

"""Configuration file management functions.

This file contains functions to manage the creation and verification of
configuration files used in SecurityCenter programs.

This file can also be run standalone to generate an example configuration file.

functions:
    create_new() -> configparser.ConfigParser:
        Generate and return an example configuration file object
        as a ConfigParser object

    validate(file: str = DEFAULT_FILE_NAME) -> (configparser.ConfigParser, Exception):
        Reads and validates the file provided to be valid config, containing all required sections.
        Returns a ConfigParser object and any exception errors

    read(file: str = DEFAULT_FILE_NAME) -> configparser.ConfigParser:
        Reads provided file, returning a ConfigParser object.

    save(config: configparser.ConfigParser, file: str = DEFAULT_FILE_NAME):
        Writes the provided ConfigParser object to a file.

constants:
    DEFAULT_FILE_NAME
        Used as a default name for all functions.

error classes:
    InvalidConfigurationFile
        Raised for a failed configuration file validation
"""

from tenable_sc_config.config import *

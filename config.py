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
from configparser import ConfigParser

DEFAULT_FILE_NAME = 'TenableSCConfig.ini'

__all__ = ['create_new', 'read', 'save', 'validate',
           'UnableToCreateFile', 'InvalidConfigurationFile', 'DEFAULT_FILE_NAME']


def create_new() -> ConfigParser:
    """Creates and returns a default ini file in a ConfigParser object"""
    config = ConfigParser(allow_no_value=True)
    xform = config.optionxform
    config.optionxform = str
    config['SecurityCenter'] = {"# Do not include http:// or https:// with 'hostname'": None}
    config.optionxform = xform
    config['SecurityCenter']['hostname'] = 'serveraddress.com'
    config['User'] = {'username': 'username'}
    xform = config.optionxform
    config.optionxform = str
    config['User']["# Valid password keys are 'password' and 'password64'"] = None
    config['User'][
        "# 'password64' is a Base64 encoded password and will be used over 'password' if both are present"] = None
    config.optionxform = xform
    config['User']['password'] = 'password'
    return config


def save(config: ConfigParser, file: str = DEFAULT_FILE_NAME):
    """Saves passed ConfigParser object to file location"""
    if not isinstance(config, ConfigParser):
        raise TypeError('ConfigParser type not passed to save_config_file')

    try:
        with open(file, 'w') as config_file:
            config.write(config_file)
    except OSError as e:
        raise OSError(f'File Error: {e}')
    except TypeError as e:
        raise TypeError(f'Invalid Parameter: {e}')


def read(file: str = DEFAULT_FILE_NAME) -> ConfigParser:
    """Attempts to read passed file and return the results in a ConfigParser object"""
    config = ConfigParser()

    try:
        config.read(file)
    except Exception as err:
        print(err)

    return config


def validate(file: str = DEFAULT_FILE_NAME) -> (ConfigParser, Exception):
    config = read(file)

    config_to_lower = {}
    for items in config:
        config_to_lower[items.lower()] = items

    if 'securitycenter' not in config_to_lower:
        return None, InvalidConfigurationFile('[SecurityCenter] section not found')
    if 'user' not in config_to_lower:
        return None, InvalidConfigurationFile('[User] section not found')

    if 'hostname' not in config[config_to_lower['securitycenter']]:
        return None, InvalidConfigurationFile('hostname parameter not found')

    if 'username' not in config[config_to_lower['user']]:
        return None, InvalidConfigurationFile('username parameter not found')
    if 'password' not in config[config_to_lower['user']] and 'password64' not in config[config_to_lower['user']]:
        return None, InvalidConfigurationFile('password parameter not found')

    return config, None


# exception classes
class Error(Exception):
    """Base class for config exceptions."""

    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__


class InvalidConfigurationFile(Error):
    """Exception for an invalid configuration file"""

    def __init__(self, msg=''):
        super(InvalidConfigurationFile, self).__init__(f'Invalid Configuration File: {msg}')


class UnableToCreateFile(Error):

    def __init__(self, msg=''):
        super(UnableToCreateFile, self).__init__(f'Unable to Create File: {msg}')


if __name__ == '__main__':

    file_name = DEFAULT_FILE_NAME
    print('Generating default example configuration file ...')
    try:
        save(config=create_new(), file=file_name)
    except Exception as e:
        raise UnableToCreateFile(e)
    print(f'File created: {file_name}')

from base64 import b64decode
from configparser import ConfigParser

DEFAULT_FILE_NAME = 'TenableSCConfig.ini'

config = None

__all__ = ['create_new', 'read', 'save', 'validate', 'load',
           'UnableToCreateFile', 'InvalidConfigurationFile',
           'DEFAULT_FILE_NAME', 'config', 'Config']


class Config:
    def __init__(self, host):
        self.host = host
        self.username = ''
        self.password = ''

    def set(self, username, password):
        self.username = username
        self.password = password


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


def validate(file: str = DEFAULT_FILE_NAME) -> (Config, Exception):
    config_to_validate = read(file)

    config_to_lower = {}
    for items in config_to_validate:
        config_to_lower[items.lower()] = items

    if 'securitycenter' not in config_to_lower:
        return None, InvalidConfigurationFile('[SecurityCenter] section not found')
    if 'user' not in config_to_lower:
        return None, InvalidConfigurationFile('[User] section not found')

    if 'hostname' not in config_to_validate[config_to_lower['securitycenter']]:
        return None, InvalidConfigurationFile('hostname parameter not found')

    if 'username' not in config_to_validate[config_to_lower['user']]:
        return None, InvalidConfigurationFile('username parameter not found')
    if 'password' not in config_to_validate[config_to_lower['user']] and 'password64' not in config_to_validate[
        config_to_lower['user']]:
        return None, InvalidConfigurationFile('password parameter not found')

    return config_to_validate, None


def load(config) -> Config:
    output = None
    if isinstance(config, str):
        config, e = validate(config)
        if e:
            raise e
    if isinstance(config, ConfigParser):
        try:
            sections = {k.lower(): v for k, v in config.items()}
            sc_section = {k.lower(): v for k, v in sections['securitycenter'].items()}
            user_section = {k.lower(): v for k, v in sections['user'].items()}
            hostname = sc_section['hostname']
            username = user_section['username']
            if 'password' in user_section.keys():
                password = user_section['password']
            if 'password64' in user_section.keys():
                password = b64decode(user_section['password64']).decode('utf-8')
            output = Config(hostname)
            output.set(username, password)
        except Exception as e:
            raise e
    else:
        raise NotImplemented(f'Unable to load file type: {type(config)}')

    return output


# exception classes
class _Error(Exception):
    """Base class for config exceptions."""

    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__


class InvalidConfigurationFile(_Error):
    """Exception for an invalid configuration file"""

    def __init__(self, msg=''):
        super(InvalidConfigurationFile, self).__init__(f'Invalid Configuration File: {msg}')


class UnableToCreateFile(_Error):

    def __init__(self, msg=''):
        super(UnableToCreateFile, self).__init__(f'Unable to Create File: {msg}')


if __name__ == '__main__':

    f = DEFAULT_FILE_NAME
    print('Generating default example configuration file ...')
    try:
        save(config=create_new(), file=f)
    except Exception as e:
        raise UnableToCreateFile(e)
    print(f'File created: {f}')
else:
    try:
        with open(DEFAULT_FILE_NAME, 'r') as f:
            loaded_config = load(f.name)
            if loaded_config:
                config = loaded_config
    except FileNotFoundError:
        pass

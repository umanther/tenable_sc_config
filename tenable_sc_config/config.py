from base64 import b64decode
from configparser import ConfigParser

from tenable_sc_config.errors import *

DEFAULT_FILE_NAME = 'TenableSCConfig.ini'

DEFAULT_VALUES = {'<server address>', '<user name>', '<password>', '<access key>', '<secret key>'}

__all__ = ['create_new', 'read', 'save', 'validate', 'load',
           'DEFAULT_FILE_NAME', 'DEFAULT_VALUES', 'config', 'SCConfig']


class SCConfig:
    def __init__(self, hostname):
        self.hostname = hostname
        self.username = None
        self.password = None
        self.access_key = None
        self.secret_key = None

    def setPword(self, username, password):
        self.username = username
        self.password = password

    def setAPI(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key

    def get(self) -> (str, (str, str)):
        if self.isnotdefault:
            if self.access_key:
                return 'api', self.getAPI()
            elif self.username:
                return 'pword', self.getPword()
            else:
                return None, None
        else:
            return None, None

    def getPword(self) -> (str, str):
        return self.username, self.password

    def getAPI(self) -> (str, str):
        return self.access_key, self.secret_key

    @property
    def isnotdefault(self):
        output = True
        if self.hostname in DEFAULT_VALUES:
            output = False
        if all([self.username, any([self.username in DEFAULT_VALUES, self.password in DEFAULT_VALUES])]) or \
                all([self.access_key, any([self.access_key in DEFAULT_VALUES, self.secret_key in DEFAULT_VALUES])]):
            output = False
        return output


config: SCConfig = None


def create_new() -> ConfigParser:
    """Creates and returns a default ini file in a ConfigParser object"""
    config = ConfigParser(allow_no_value=True)
    xform = config.optionxform
    config.optionxform = str
    config['SecurityCenter'] = {"# Do not include http:// or https:// with 'hostname'": None}
    config.optionxform = xform
    config['SecurityCenter']['hostname'] = '<server address>'
    config.optionxform = str
    config['User'] = {"# API keys, if present, will be used over a username/password configuration": None}
    config['User'][
        "# It is not necessary to include both username/password and API keys."
        "  Include whichever pair you intend to use"] = None
    config.optionxform = xform
    config['User']['username'] = '<user name>'
    config.optionxform = str
    config['User']["# Valid password keys are 'password' and 'password64'"] = None
    config['User'][
        "# 'password64' is a Base64 encoded password and will be used over 'password' if both are present"] = None
    config.optionxform = xform
    config['User']['password'] = '<password>'
    config['User']['access_key'] = '<access key>'
    config['User']['secret_key'] = '<secret key>'
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


def validate(file: str = DEFAULT_FILE_NAME) -> (SCConfig, Exception):
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

    if 'username' in config_to_validate[config_to_lower['user']]:
        if 'password' not in config_to_validate[config_to_lower['user']] and 'password64' not in config_to_validate[
            config_to_lower['user']]:
            return None, InvalidConfigurationFile('username provided but password parameter not found')
    elif 'access_key' in config_to_validate[config_to_lower['user']]:
        if 'secret_key' not in config_to_validate[config_to_lower['user']]:
            return None, InvalidConfigurationFile('api access key provided but secret key parameter not found')
    else:
        return None, InvalidConfigurationFile('configuration file must include username/password or API keypair')

    return config_to_validate, None


def load(config) -> SCConfig:
    output = None
    if isinstance(config, str):
        config, e = validate(config)
        if e:
            raise e
    if isinstance(config, ConfigParser):
        username = None
        password = None
        access_key = None
        secret_key = None

        try:
            sections = {k.lower(): v for k, v in config.items()}
            sc_section = {k.lower(): v for k, v in sections['securitycenter'].items()}
            user_section = {k.lower(): v for k, v in sections['user'].items()}
            hostname = sc_section['hostname']
            if 'access_key' in user_section:
                access_key = user_section['access_key']
                secret_key = user_section['secret_key']
            if 'username' in user_section:
                username = user_section['username']
                if 'password' in user_section.keys():
                    password = user_section['password']
                if 'password64' in user_section.keys():
                    password = b64decode(user_section['password64']).decode('utf-8')
            output = SCConfig(hostname)
            if username:
                output.setPword(username, password)
            if access_key:
                output.setAPI(access_key, secret_key)
        except Exception as e:
            raise e
    else:
        raise NotImplemented(f'Unable to load file type: {type(config)}')

    return output


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
                if loaded_config.isnotdefault:
                    config = loaded_config
                else:
                    raise InvalidConfigurationFile('Contains default values.')
    except FileNotFoundError:
        pass

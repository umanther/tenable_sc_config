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

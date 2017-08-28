"""Return various facts for string formatting.
"""
import socket
from collections import MutableMapping

from six import string_types


class Facts(MutableMapping):
    """A dict-like object that evaluates values at access time."""

    def __init__(self, config=None, **kwargs):
        self.__dict__ = {}
        self.__set_defaults(config)
        self.__set_config(config)
        self.__dict__.update(dict(**kwargs))

    def __set_defaults(self, config):
        defaults = {
            'server_name': lambda: config.server_name,
            'server_id': None,
            'process_num': None,
            'pool_nane': None,
            'fqdn': lambda: socket.getfqdn(),
            'hostname': lambda: socket.gethostname().split('.', 1)[0],
        }
        self.__dict__.update(defaults)

    def __set_config(self, config):
        if config is not None:
            for name in dir(config):
                if not name.startswith('_') and isinstance(getattr(config, name), string_types):
                    self.__dict__['config_' + name] = lambda name=name: getattr(config, name)

    def __getitem__(self, key):
        #item = super(Facts, self).__getitem__(key)
        item = self.__dict__.__getitem__(key)
        if callable(item):
            return item()
        else:
            return item

    # Other methods pass through to the corresponding dict methods

    def __setitem__(self, key, value):
        return self.__dict__.__setitem__(key, value)

    def __delitem__(self, key):
        return self.__dict__.__delitem__(key)

    def __iter__(self):
        return self.__dict__.__iter__()

    def __len__(self):
        return self.__dict__.__len__()


def get_facts(config=None, **kwargs):
    return Facts(config=config, **kwargs)

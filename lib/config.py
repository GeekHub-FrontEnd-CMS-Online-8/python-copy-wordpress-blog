#!/usr/bin/env python

import os

try:
    import ConfigParser as configparser
except ModuleNotFoundError:
    import configparser


def get_config(file):

    config = configparser.ConfigParser()
    config_file = os.path.join(os.getcwd(), 'conf', file)

    with open(config_file):
        config.read(config_file)

    return config

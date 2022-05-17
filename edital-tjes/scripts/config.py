"""
-> Obtêm e salva as configurações disponíveis para o usuário.
"""

from __future__ import absolute_import

from distutils.util import strtobool
import configparser


def load_color_scheme() -> bool:
    config = configparser.ConfigParser()

    config.read('./edital-tjes/data/config.ini')
    return strtobool(config.get('DEFAULT', 'dark_mode'))


def save_color_scheme(status: str) -> None:
    config = configparser.ConfigParser()
    config.read('./edital-tjes/data/config.ini')

    config.set('DEFAULT', 'dark_mode', status)

    with open('./edital-tjes/data/config.ini', 'w+') as file:
        config.write(file)

import os
import re

from abc import ABC, abstractmethod
import utils

modes = ['power-saving', 'balanced']


def is_powersaved():
    return os.path.exists('/etc/modprobe.d/block-nvidia.conf') or os.path.exists('/lib/udev/rules.d/50-disable-nvidia.rules')


def set_powersaved(state):
    if state:
        utils.create_symlink(utils.get_config_filepath('block-nvidia.conf'), '/etc/modprobe.d/block-nvidia.conf')
        utils.create_symlink(utils.get_config_filepath('50-disable-nvidia.rules'), '/lib/udev/rules.d/50-disable-nvidia.rules')
    else:
        utils.remove('/etc/modprobe.d/block-nvidia.conf')
        utils.remove('/lib/udev/rules.d/50-disable-nvidia.rules')
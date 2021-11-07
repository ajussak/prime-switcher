#!/usr/bin/env python3

import argparse
import gui
import utils
import switcher
import os
import gettext

def run_as_root(func, *args, **kwargs) -> None:
    """Check if user is root and execute given function else PermissionError"""
    if os.getuid() == 0:
        func(*args, **kwargs)
    else:
        raise PermissionError('Root permissions are required.')


def main():
    localedir = utils.get_debug_path('locales') if os.getenv('DEBUG', 0) else None
    gettext.install('prime-switcher', localedir=localedir)

    parser = argparse.ArgumentParser(prog='prime-switcher')
    parser.add_argument('--set', '-s', type=str, choices=switcher.modes)
    parser.add_argument('--uninstall', '-u', action='store_true')
    parser.add_argument('--gui', action='store_true')
    parser.add_argument('--query', '-q', action='store_true')
    args = parser.parse_args()

    if args.gui:
        gui.open_gui()
    elif args.query:
        gpu = 'Power Saving' if switcher.is_powersaved() else 'Balanced'
        print('Current Mode :', gpu)
    elif args.uninstall:
        print('Uninstalling...')
        run_as_root(switcher.set_powersaved, False)
        print('Done.')
    elif args.set is not None:
        print('Configuring...')
        run_as_root(switcher.set_powersaved, args.set == 'power-saving')
        print('Done. Reboot required to apply changes.')
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

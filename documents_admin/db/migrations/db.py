#!/usr/bin/env python
import argparse
import os
import sys
from os.path import dirname, join, realpath

from alembic import command
from alembic.config import Config
from sqlalchemy.exc import OperationalError


def parse_arguments():
    parser = argparse.ArgumentParser(description='Alembic runner')
    parser.add_argument(
        '-e',
        '--env',
        default=None,
        choices=LOCAL_DATABASES,
        help='Optional environment setting'
    )
    parser.add_argument(
        'command',
        choices=ALEMBIC_COMMANDS,
        help='Alembic command to be executed'
    )
    parser.add_argument(
        'options',
        nargs='*',
        help='Additional options to pass alongisde alembic command'
    )

    return parser.parse_args()


def handle_operational_error(e):
    print('Cannot connect to database.')
    print(e)
    sys.exit(1)


def downgrade(alembic_cfg, options):
    if not options:
        options = '-1'
    try:
        command.downgrade(alembic_cfg, options)
    except OperationalError as e:
        handle_operational_error(e)


def upgrade(alembic_cfg, options):
    if not options:
        options = 'head'
    try:
        command.upgrade(alembic_cfg, options)
    except OperationalError as e:
        handle_operational_error(e)


def migrate(alembic_cfg, message):
    if not message:
        print('Please provide migration message, thanks.')
        sys.exit(1)
    try:
        command.revision(alembic_cfg, message=message, autogenerate=True)
    except OperationalError as e:
        handle_operational_error(e)


def run_alembic(db_url, cmd, options):
    script_location = (dirname(realpath(__file__)))
    config_location = join(script_location, 'alembic.ini')
    print(script_location, config_location)
    alembic_cfg = Config(config_location)
    alembic_cfg.set_main_option('script_location', script_location)
    alembic_cfg.set_main_option('sqlalchemy.url', db_url)

    ALEMBIC_COMMANDS[cmd](alembic_cfg, options)


# default local databases (first one is considered a 'default' one)
LOCAL_DATABASES = {
    'development': 'sqlite:///documents.sqlite',
}

# supported alembic commands
ALEMBIC_COMMANDS = {
    'downgrade': downgrade,
    'upgrade': upgrade,
    'migrate': migrate,
}

if __name__ == '__main__':
    args = parse_arguments()
    alembic_cmd = args.command
    alembic_options = ' '.join(args.options)

    if alembic_cmd == 'migrate':
        databases = [LOCAL_DATABASES['development']]
    else:
        if args.env in LOCAL_DATABASES:
            databases = [LOCAL_DATABASES[args.env]]
        else:
            databases = list(LOCAL_DATABASES.values())

    for db_url in databases:
        print(f'Database: {db_url}...')
        run_alembic(db_url, alembic_cmd, alembic_options)

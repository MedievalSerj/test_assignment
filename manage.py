import os
import uuid

from flask_script import Manager
from flask_security.utils import encrypt_password

from documents_admin.db.migrations.db import run_alembic
from documents_admin.db.models import Role, Source, User
from documents_admin.instance import app, user_datastore

manager = Manager(app)


@manager.command
def create_roles():
    """
    adds user and admin roles to the roles table
    """
    session = app.db_session
    admin_role = Role(name='admin')
    user_role = Role(name='user')
    session.add(admin_role)
    session.add(user_role)
    session.commit()
    session.close()


def _create_default_user():
    session = app.db_session
    admin_role = session.query(Role).filter(Role.name == 'admin').first()
    admin_user = User(active=1,
                      roles=[admin_role, ],
                      email='admin',
                      username='admin',
                      password=encrypt_password('admin'))
    source = Source(sid=str(uuid.uuid1()),
                    name='default source',
                    url='www.example.com')
    session.add(admin_user)
    session.add(source)
    session.commit()
    session.close()


@manager.command
def create_all():
    """Run migrations, create roles, add default user"""
    run_alembic(app.config['DB_URL'], 'upgrade', 'head')
    create_roles()
    _create_default_user()


@manager.command
def create_admin():
    """
    create a new admin user
    """
    fields = {'email': None,
              'username': None,
              'password': None}
    session = app.db_session
    for key in fields.keys():
        fields[key] = input(f'enter {key}: ')
    fields['password'] = encrypt_password(fields['password'])
    admin_role = session.query(Role).filter(Role.name == 'admin').first()
    admin_user = user_datastore.create_user(active=1, roles=[admin_role, ], **fields)
    app.db_session.add(admin_user)
    app.db_session.commit()


@manager.option('-m', '--message', dest='message', required=True,
                help='migrate massage')
def migrate(message):
    """Usage:
    python manage.py migrate -m initial
    """
    run_alembic(app.config['DB_URL'], 'migrate', message)


@manager.option('-r', '--revision', dest='revision', default='head',
                help='revision or "head"')
def upgrade(revision):
    """Usage:
    python manage.py upgrade -r head
    """
    run_alembic(app.config['DB_URL'], 'upgrade', revision)


@manager.option('-r', '--revision', dest='revision', required=True,
                help='revision')
def downgrade(revision):
    """Usage:
    python manage.py downgrade -r cc537ef09e40
    """
    run_alembic(app.config['DB_URL'], 'upgrade', revision)


@manager.command
def clean_all():
    """
    delete db
    """
    os.remove('documents.sqlite')


if __name__ == '__main__':
    manager.run()

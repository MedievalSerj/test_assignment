from flask_script import Manager
from documents_admin.instance import app
from documents_admin.db.migrations.db import run_alembic
from documents_admin.db.models import Role, User, Source
from documents_admin.instance import user_datastore
from flask_security.utils import encrypt_password
import os
import glob
import uuid


manager = Manager(app)
DB_URL = 'sqlite:///documents.sqlite'


@manager.command
def clean_all():
    """
    delete db and migrations
    """
    filelist = glob.glob(os.path.join(
        'documents_admin/db/migrations/versions', "*.py"))
    for f in filelist:
        os.remove(f)
    os.remove('documents.sqlite')


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


@manager.command
def create_all():
    run_alembic(DB_URL, 'migrate', 'initial')
    run_alembic(DB_URL, 'upgrade', 'head')
    create_roles()


@manager.command
def create_all_dev():
    run_alembic(DB_URL, 'migrate', 'initial')
    run_alembic(DB_URL, 'upgrade', 'head')
    create_roles()
    session = app.db_session
    admin_role = session.query(Role).filter(Role.name == 'admin').first()
    admin_user = User(active=1,
                      roles=[admin_role,],
                      email='ladonya.s@gmail.com',
                      username='serj',
                      password=encrypt_password('123'))
    source = Source(sid=str(uuid.uuid1()),
                    name='default source',
                    url='www.be-be-be-me-me-me-fur-fur-fur')
    session.add(admin_user)
    session.add(source)
    session.commit()
    session.close()


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
    admin_role = session.query(Role).filter(Role.name=='admin').first()
    admin_user = user_datastore.create_user(active=1, roles=[admin_role, ], **fields)
    app.db_session.add(admin_user)
    app.db_session.commit()


@manager.option('-m', '--message', dest='message', required=True,
                help='migrate massage')
def migrate(message):
    """Usage:
    python manage.py migrate -m initial
    """
    run_alembic(DB_URL, 'migrate', message)


@manager.option('-r', '--revision', dest='revision', default='head',
                help='revision or "head"')
def upgrade(revision):
    """Usage:
    python manage.py upgrade -r head
    """
    run_alembic(DB_URL, 'upgrade', revision)


@manager.option('-r', '--revision', dest='revision', required=True,
                help='revision')
def downgrade(revision):
    """Usage:
    python manage.py downgrade -r cc537ef09e40
    """
    run_alembic(DB_URL, 'upgrade', revision)


if __name__ == '__main__':
    manager.run()

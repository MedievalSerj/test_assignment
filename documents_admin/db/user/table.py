import sqlalchemy as sa
from ..core import metadata


user_table = sa.Table(
    'user',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('email', sa.String, unique=True, nullable=False),
    sa.Column('username', sa.String, unique=True, nullable=False),
    sa.Column('password', sa.String, nullable=False),
    sa.Column('active', sa.Boolean, nullable=False, default=False),
    sa.Index('user_email_idx',
             'email'),
    sa.Index('user_username_idx',
             'username')
)

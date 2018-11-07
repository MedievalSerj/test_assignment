import sqlalchemy as sa
from ..core import metadata


role_table = sa.Table(
    'role',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(64), unique=True),
    sa.Index('role_name_idx',
             'name')
)

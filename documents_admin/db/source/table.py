import uuid

import sqlalchemy as sa

from ..core import metadata

source_table = sa.Table(
    'source',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('sid', sa.String, unique=True, default=str(uuid.uuid1())),
    sa.Column('name', sa.String, unique=True, nullable=False),
    sa.Column('url', sa.String, nullable=False),
    sa.Index('source_name_idx',
             'name'),
    sa.Index('source_sid_idx',
             'sid')
)

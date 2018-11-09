from time import time

import sqlalchemy as sa

from ..core import metadata

document_table = sa.Table(
    'document',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('source_id', sa.Integer, sa.ForeignKey('source.id',
                                                     ondelete='CASCADE',
                                                     onupdate='CASCADE'),
              nullable=False),
    sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id',
                                                   ondelete='CASCADE',
                                                   onupdate='CASCADE'),
              nullable=False),
    sa.Column('title', sa.String, nullable=False),
    sa.Column('text', sa.String, nullable=False),
    sa.Column('url', sa.String, nullable=False),
    sa.Column('created', sa.DateTime, nullable=False),
    sa.Column('added_at', sa.Integer, default=int(time())),
    sa.Column('updated', sa.Integer, onupdate=int(time()),
              default=int(time())),
    sa.Column('times_edited', sa.Integer, default=0),
    sa.Index('document_title_text_unique_idx',
             'title',
             'text',
             unique=True)
)

import sqlalchemy as sa
from ..core import metadata
from datetime import datetime

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
    sa.Column('title', sa.String(128), nullable=False),
    sa.Column('text', sa.String, nullable=False),
    sa.Column('url', sa.String(256), nullable=False),
    sa.Column('created', sa.DateTime),
    sa.Column('created_at', sa.DateTime, default=datetime.utcnow),
    sa.Column('updated', sa.DateTime, onupdate=datetime.utcnow),
    sa.Index('document_title_text_unique_idx',
             'title',
             'text',
             unique=True)
)

import sqlalchemy as sa
from ..core import metadata


user_role_info_table = sa.Table(
    'user_role_info',
    metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id',
                                                   onupdate='CASCADE',
                                                   ondelete='CASCADE'),
              nullable=False),
    sa.Column('role_id', sa.Integer, sa.ForeignKey('role.id',
                                                   onupdate='CASCADE',
                                                   ondelete='CASCADE'),
              nullable=False),
    sa.Index('user_role_info_user_id_idx',
             'user_id'),
    sa.Index('user_role_info_role_id_idx',
             'role_id'),
)

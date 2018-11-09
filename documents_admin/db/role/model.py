from sqlalchemy.orm import relationship

from ..core import Base
from ..user_role_info import user_role_info_table
from .table import role_table


class Role(Base):

    __table__ = role_table

    users = relationship('User',
                         back_populates='roles',
                         secondary=user_role_info_table)

    def __repr__(self):
        return self.name

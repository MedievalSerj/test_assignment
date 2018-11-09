from flask_security import UserMixin
from sqlalchemy.orm import relationship

from ..core import Base
from ..user_role_info import user_role_info_table
from .table import user_table


class User(Base, UserMixin):

    __table__ = user_table

    roles = relationship('Role',
                         back_populates='users',
                         secondary=user_role_info_table)
    documents = relationship('Document',
                             back_populates='user',
                             cascade='all, delete-orphan')

    def get_id(self):
        return self.id

    def __repr__(self):
        return self.username

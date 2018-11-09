from sqlalchemy.orm import relationship

from ..core import Base
from .table import document_table


class Document(Base):

    __table__ = document_table

    source = relationship('Source', back_populates='documents')
    user = relationship('User', back_populates='documents')

    def __repr__(self):
        return self.title

from sqlalchemy.orm import relationship

from ..core import Base
from .table import source_table


class Source(Base):

    __table__ = source_table

    documents = relationship('Document',
                             back_populates='source',
                             cascade='all, delete-orphan')

    def __repr__(self):
        return self.name

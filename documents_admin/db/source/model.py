from ..core import Base
from .table import source_table
from sqlalchemy.orm import relationship


class Source(Base):

    __table__ = source_table

    documents = relationship('Document',
                             back_populates='source',
                             cascade='all, delete-orphan')

    def __repr__(self):
        return self.name

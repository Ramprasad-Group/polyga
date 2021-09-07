from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Text, String, JSON, Boolean, Float

Base = declarative_base()

class Polymer(Base):
    """Defines polymer"""
    __tablename__ = "polymer"

    planetary_id = Column(Integer, primary_key=True, unique=True)
    parent_1_id = Column(Integer, nullable=False)
    parent_2_id = Column(Integer, nullable=False)
    is_parent = Column(Boolean, nullable=False)
    num_chromosomes = Column(Integer, nullable=False)
    smiles_string = Column(String(1000), nullable=False)
    birth_land = Column(String(255), nullable=False)
    birth_nation = Column(String(255), nullable=False)
    birth_planet = Column(String(255), nullable=False)
    str_chromosome_ids = Column(String(255), nullable=False)
    generation = Column(Integer, nullable=False)
    settled_planet = Column(String(255), nullable=False)
    settled_land = Column(String(255), nullable=False)
    settled_nation = Column(String(255), nullable=False)
    fingerprint = Column(JSON, nullable=False)
    properties = Column(JSON, nullable=False)

    def __repr__(self):
        return f"{self.smiles_string}"

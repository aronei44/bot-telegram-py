from sqlalchemy import Column, Integer, String
from database import Base

class Roles(Base):
    __tablename__ = 'roles'
    
    role_name = Column(String, primary_key = True, unique=True)
    min_val = Column(Integer, nullable=True)
    max_val = Column(Integer, nullable=True)

    def __init__(self, role_name, min_val, max_val):
        self.role_name = role_name
        self.min_val = min_val
        self.max_val = max_val
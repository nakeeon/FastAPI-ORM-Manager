from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# A sample User model for demonstration
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    lastname = Column(String)


class UserScheme(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

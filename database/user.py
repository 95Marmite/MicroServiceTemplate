from sqlalchemy import Column, Integer, String
from database.database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

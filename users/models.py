from sqlalchemy import Column, Integer, String, Float

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    success_requests_count = Column(Integer)
    failed_requests_count = Column(Integer)
    total_success_requests_count = Column(Float, default=0.0)
    total_failed_requests_count = Column(Float, default=0.0)
    rate_limited_requests_count = Column(Integer, default=0)

from pydantic import BaseModel


class BaseUser(BaseModel):
    id: int
    username: str
    success_requests_count: int
    failed_requests_count: int
    total_success_requests_count: float
    total_failed_requests_count: float


class User(BaseModel):
    username: str
    success_requests_count: int
    failed_requests_count: int
    total_success_requests_count: float
    total_failed_requests_count: float


class UserList(BaseModel):
    id: int
    success_requests_count: int
    failed_requests_count: int
    total_success_requests_count: float
    total_failed_requests_count: float
    rate_limited_requests_count: int

import time
from functools import wraps

import requests

from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session

from users import crud

from dependencies import get_db
from users.models import User
from users.schemas import UserList

router = APIRouter()


def rate_limited(max_calls: int, time_frame: int):
    def decorator(func):
        user_calls = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            username = kwargs.get("username")
            db = kwargs.get("db")

            if username not in user_calls:
                user_calls[username] = []

            calls_in_time_frame = [call for call in user_calls[username] if call > now - time_frame]
            if len(calls_in_time_frame) >= max_calls:
                db_user = db.query(User).filter(User.username == username).first()
                db_user.rate_limited_requests_count += 1
                db.commit()
                db.refresh(db_user)

                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                                    detail=f"rate limit exceeded")
            user_calls[username].append(now)
            return func(*args, **kwargs)

        return wrapper

    return decorator


@router.get("/user/{username}/url/{address:path}", response_model=dict)
@rate_limited(max_calls=5, time_frame=60)
def get_response(username: str, address: str, db: Session = Depends(get_db)):
    start_time = time.time()
    status = "success"
    try:
        res = requests.get(f"http://{address}")
        response_time = time.time() - start_time
        if str(res.status_code)[0] in "45":
            status = "fail"
    except requests.exceptions.RequestException as e:
        response_time = time.time() - start_time
        status = "fail"

    response_dict = {
        "username": username,
        "status": status,
        "seconds_of_response": response_time * 1000
    }
    return crud.create_request(db=db, response=response_dict)


@router.get("/user/{username}/stats", response_model=dict)
def get_user_stats(username: str, db: Session = Depends(get_db)):
    return crud.user_stats(db=db, username=username)


@router.get("/stats", response_model=list[UserList])
def get_all_stats(db: Session = Depends(get_db)):
    return crud.get_stats(db=db)

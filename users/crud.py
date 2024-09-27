from typing import List, Type

from sqlalchemy.orm import Session

from users.models import User


def create_request(db: Session, response: dict) -> dict:
    db_user = db.query(User).filter(User.username == response["username"]).first()

    if db_user:
        if response["status"] == "fail":
            db_user.failed_requests_count += 1
            db_user.total_failed_requests_count += response["seconds_of_response"]
        else:
            db_user.success_requests_count += 1
            db_user.total_success_requests_count += response["seconds_of_response"]
    else:
        if response["status"] == "fail":
            db_user = User(
                username=response["username"],
                success_requests_count=0,
                failed_requests_count=1,
                total_success_requests_count=0.0,
                total_failed_requests_count=response["seconds_of_response"],
                rate_limited_requests_count=0
            )
        else:
            db_user = User(
                username=response["username"],
                success_requests_count=1,
                failed_requests_count=0,
                total_success_requests_count=response["seconds_of_response"],
                total_failed_requests_count=0.0,
                rate_limited_requests_count=0
            )
        db.add(db_user)

    db.commit()
    db.refresh(db_user)
    # return db_user
    return {
        "seconds": response["seconds_of_response"],
    }


def user_stats(db: Session, username: str) -> dict:
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        return {"status": "fail", "info": "no such user"}

    average_request_time = (
            (db_user.total_success_requests_count + db_user.total_failed_requests_count)
            / (db_user.success_requests_count + db_user.failed_requests_count))

    return {
        "number of successful requests": db_user.success_requests_count,
        "number of failed requests": db_user.failed_requests_count,
        "average request time": average_request_time
    }


def get_stats(db: Session) -> list[Type[User]]:
    return db.query(User).all()

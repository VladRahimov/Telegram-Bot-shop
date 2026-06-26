from datetime import datetime, timedelta


def set_session_expire(data: dict, minutes: int):
    data["expires_at"] = datetime.now() + timedelta(minutes=minutes)


def is_session_expired(data: dict) -> bool:
    expires_at = data.get("expires_at")

    if expires_at is None:
        return False

    return datetime.now() > expires_at
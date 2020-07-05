from datetime import datetime, timedelta

from pytz import utc, timezone


KST = timezone("Asia/Seoul")


def get_plus1day_datetime() -> datetime:
    return now_utc() + timedelta(days=1)


def get_expiring_datetime():
    return get_plus1day_datetime()


def now_utc() -> datetime:
    return utc.localize(datetime.utcnow())


def now_seoul() -> datetime:
    return now_utc().astimezone(KST)

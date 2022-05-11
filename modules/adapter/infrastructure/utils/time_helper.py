from datetime import datetime
from zoneinfo import ZoneInfo


def get_server_timestamp() -> datetime:
    utc: datetime = datetime.utcnow()
    kst: datetime = utc.astimezone(ZoneInfo("Asia/Seoul"))
    return kst

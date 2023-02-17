from datetime import datetime, timezone, timedelta
from pathlib import Path


def create_directory(path: str | Path):
    """
    创建指定路径的目录。

    Args:
        path (str): 目录路径。
    """
    # if not isinstance(path, str):
    #     path = path.__str__()
    if not Path(path).exists():
        Path(path).mkdir()



def local_date():
    bj_time = (
        datetime.utcnow()
        .replace(tzinfo=timezone.utc)
        .astimezone(timezone(timedelta(hours=8)))
    )
    path_time = bj_time.strftime("%Y-%m-%d")
    print(path_time,type(path_time))
    return path_time


class SingletonDecorator:
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwds):
        if self.instance is None:
            self.instance = self.cls(*args, **kwds)
        return self.instance

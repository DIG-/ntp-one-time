from sys import platform


def _update_system_time_linux(value: int):
    raise NotImplementedError("Can not update time to your system, yet")


def _update_system_time_windows(value: int):
    from datetime import datetime

    from win32api import SetSystemTime

    utc = datetime.utcfromtimestamp(value)
    SetSystemTime(utc.year, utc.month, utc.weekday(), utc.day, utc.hour, utc.minute, utc.second, 0)


def update_system_time(value: int):
    if platform.startswith("win32") or platform.startswith("cygwin"):
        return _update_system_time_windows(value)
    if platform.startswith("linux"):
        return _update_system_time_linux(value)
    raise NotImplementedError("Can not update time to your system")

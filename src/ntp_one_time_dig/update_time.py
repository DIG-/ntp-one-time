from subprocess import run
from sys import platform


def _update_system_time_linux(value: int, restart: bool, restart_now: bool):
    raise NotImplementedError("Can not update time to your system, yet")


def _update_system_time_windows(value: int, restart: bool, restart_now: bool):
    from datetime import datetime

    from win32api import SetSystemTime

    utc = datetime.utcfromtimestamp(value)
    SetSystemTime(utc.year, utc.month, utc.weekday(), utc.day, utc.hour, utc.minute, utc.second, 0)
    if restart:
        run(
            " ".join(
                (
                    "shutdown",
                    "/r",
                    "/f",
                    "/t",
                    "0" if restart_now else "90",
                    "/c",
                    '"Restarting computer to apply new date and time. Save everything."',
                )
            ),
            shell=True,
        )
        pass


def update_system_time(value: int, restart: bool, restart_now: bool):
    if platform.startswith("win32") or platform.startswith("cygwin"):
        return _update_system_time_windows(value, restart, restart_now)
    if platform.startswith("linux"):
        return _update_system_time_linux(value, restart, restart_now)
    raise NotImplementedError("Can not update time to your system")

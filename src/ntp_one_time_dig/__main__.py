from getopt import GetoptError, gnu_getopt
from sys import argv
from time import ctime, sleep, time

from ntplib import NTPClient, NTPException

from .update_time import update_system_time

timeout = 5
repeat = 10
delay = 3
increment = 5

try:
    options, server_list = gnu_getopt(argv[1:], "t:r:d:i:", ["timeout=", "repeat=", "delay=", "increment="])
except GetoptError as error:
    print(error)
    exit(1)

if len(server_list) <= 0:
    print("Require server url")
    exit(2)

for option, value in options:
    if option in ("-t", "--timeout"):
        timeout = int(value)
    elif option in ("-r", "--repeat"):
        repeat = int(value)
    elif option in ("-d", "--delay"):
        delay = int(value)
    elif option in ("-i", "--increment"):
        increment = int(value)

client = NTPClient()
started = time()
for i in range(1, repeat):
    print(f"Try {i}")
    for server in server_list:
        print(f" Server {server}")
        try:
            stats = client.request(server, timeout=timeout)
        except NTPException:
            continue
        except BaseException as error:
            print(f"  Failed: {error}")
            continue
        if stats.offset < 1 and stats.offset > -1:
            print("Time is almost exact, nothing to do!")
            exit(0)
        new_time = int(time() + stats.offset)
        print(f"Adjust time to: {ctime(new_time)}")

        update_system_time(new_time, abs(stats.offset) > (24 * 60 * 60), (time() - started) < 90)
        exit(0)
    print(f"Wait {delay} seconds")
    sleep(delay)
    delay += increment
print("Exhausted")
exit(3)

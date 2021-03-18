import time
from croniter import croniter

def get_next_schedule_time(schedule_or_schedules, now = time.time()):
    if type(schedule_or_schedules) is not list:
        schedule_or_schedules = [schedule_or_schedules]

    def convert_to_seconds(duration):
        seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
        return int(duration[:-1]) * seconds_per_unit[duration[-1].lower()]

    def _lambda(schedule):
        if ' ' in schedule:
            return croniter(schedule, now).get_next()
        return convert_to_seconds(schedule) + now

    times = list(map(_lambda, schedule_or_schedules))

    return round(sorted(times)[0])

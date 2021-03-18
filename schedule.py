import time, threading, sched
from croniter import croniter

def get_next_schedule_time(schedule_or_schedules, now = None):
    if not now:
        now = time.time()
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

def schedule_once(schedule_or_schedules, fn, args = (), kwargs={}, on_error = None):
    def _action():
        try:
            fn(*args, **kwargs)
        except Exception as e:
            if on_error:
                on_error(e)
            else:
                raise e

    scheduler = sched.scheduler(time.time)
    evt = scheduler.enterabs(get_next_schedule_time(schedule_or_schedules), 1, _action)
    scheduler.run()

    return lambda: scheduler.cancel(evt)

def schedule(schedule_or_schedules, fn, args = (), kwargs={}, on_error = None):
    evt = None

    def _action():
        _schedule_next()
        try:
            fn(*args, **kwargs)
        except Exception as e:
            if on_error:
                on_error(e)
            else:
                raise e

    def _schedule_next():
        evt = scheduler.enterabs(get_next_schedule_time(schedule_or_schedules), 1, _action)

    scheduler = sched.scheduler(time.time)
    _schedule_next()
    scheduler.run()

    return lambda: scheduler.cancel(evt)

def schedule_once_in_thread(schedule_or_schedules, fn, args = (), kwargs={}, on_error = None):
    threading.Thread(
        target=schedule_once,
        kwargs={
            'schedule_or_schedules': schedule_or_schedules,
            'fn': fn,
            'args': args,
            'kwargs': kwargs,
            'on_error': on_error
        }
    ).start()

    #return lambda: raise Exception('Not handled')

def schedule_in_thread(schedule_or_schedules, fn, args = (), kwargs={}, on_error = None):
    threading.Thread(
        target=schedule,
        kwargs={
            'schedule_or_schedules': schedule_or_schedules,
            'fn': fn,
            'args': args,
            'kwargs': kwargs,
            'on_error': on_error
        }
    ).start()

    #return lambda: raise Exception('Not handled')

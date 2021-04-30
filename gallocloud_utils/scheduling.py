import time, threading, sched
from croniter import croniter
from gallocloud_utils.convertions import convert_to_seconds

def get_next_schedule_time(schedule_or_schedules, now = None):
    if not now:
        now = time.time()
    if type(schedule_or_schedules) is not list:
        schedule_or_schedules = [schedule_or_schedules]


    def _lambda(schedule):
        if ' ' in schedule:
            return croniter(schedule, now).get_next()
        return convert_to_seconds(schedule) + now

    times = list(map(_lambda, schedule_or_schedules))

    return round(sorted(times)[0])

def create_scheduler():
    return sched.scheduler(time.time)

def schedule_once(schedule_or_schedules, fn, args = (), kwargs={}, on_error = None, scheduler=None):
    def _action():
        try:
            fn(*args, **kwargs)
        except Exception as e:
            if on_error:
                on_error(e)
            else:
                raise e

    provided_scheduler = bool(scheduler)
    scheduler = scheduler or create_scheduler()
    evt = scheduler.enterabs(get_next_schedule_time(schedule_or_schedules), 1, _action)
    if not provided_scheduler:
        scheduler.run()

    return lambda: scheduler.cancel(evt)

def schedule(schedule_or_schedules, fn, args = (), kwargs={}, on_error = None, runAtBegin = False, scheduler=None):
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

    provided_scheduler = bool(scheduler)
    scheduler = scheduler or create_scheduler()
    _action() if runAtBegin else _schedule_next()
    if not provided_scheduler:
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

def schedule_in_thread(schedule_or_schedules, fn, args = (), kwargs={}, on_error = None, runAtBegin = False):
    threading.Thread(
        target=schedule,
        kwargs={
            'schedule_or_schedules': schedule_or_schedules,
            'fn': fn,
            'args': args,
            'kwargs': kwargs,
            'on_error': on_error,
            'runAtBegin': runAtBegin
        }
    ).start()

    #return lambda: raise Exception('Not handled')

import unittest
import schedule
import threading

class TestStringMethods(unittest.TestCase):

    def test_get_next_schedule_time(self):
        now = 1616086475
        print('now', now)
        print('each 10s, should be 1616086485', schedule.get_next_schedule_time('10s', now))
        print('each 10th of seconds, should be 1616086480', schedule.get_next_schedule_time('* * * * * */10', now))
        print('Both of previous, should be nearest 1616086480', schedule.get_next_schedule_time([
            '10s',
            '* * * * * */10'
        ], now))

        print('Complex case, should be 1616086800', schedule.get_next_schedule_time([
            '* * * * sun',
            '0 * * * thu',
        ], now))

    def test_schedule_once(self):
        def my_action(name):
            if name == 'Paul':
                raise Exception('Bad name')
            print('hello ' + name)

        def on_error(e):
            print('Error handled', e)

        schedule.schedule_once('1s', my_action, args = ('Jean', ), kwargs={}, on_error =on_error)
        schedule.schedule_once('1s', my_action, args = ('Paul', ), kwargs={}, on_error =on_error)

        schedule.schedule_once_in_thread('1s', my_action, args = ('Jean', ), kwargs={}, on_error =on_error)

if __name__ == '__main__':
    unittest.main()

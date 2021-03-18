import unittest
import schedule

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
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

if __name__ == '__main__':
    unittest.main()

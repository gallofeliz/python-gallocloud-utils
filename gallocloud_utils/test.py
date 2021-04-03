import unittest
import scheduling
import threading
import config
import yamlconfig

class TestStringMethods(unittest.TestCase):

    def test_config_from_env(self):
        def format(values):
            for name in values['backup']:
                backup = values['backup'][name]
                backup['excludes'] = backup['excludes'].split(',')
            return values

        print(config.load_config_from_env({
            'BACKUP_MAIN_PATHS': '/directory',
            'BACKUP_MAIN_EXCLUDES': '.git,.sync',
            'BACKUP_MAIN_SCHEDULE': '*/5 * * * *',
            'CHECK_SCHEDULE': '2m',
            'GLOBAL_UPLOADLIMIT': '50K',
            'GLOBAL_DOWNLOADLIMIT': '200K',
            'SINGLE': 'yes'
        }, format))

    def test_get_next_schedule_time(self):
        now = 1616086475
        print('now', now)
        print('each 10s, should be 1616086485', scheduling.get_next_schedule_time('10s', now))
        print('each 10th of seconds, should be 1616086480', scheduling.get_next_schedule_time('* * * * * */10', now))
        print('Both of previous, should be nearest 1616086480', scheduling.get_next_schedule_time([
            '10s',
            '* * * * * */10'
        ], now))

        print('Complex case, should be 1616086800', scheduling.get_next_schedule_time([
            '* * * * sun',
            '0 * * * thu',
        ], now))

    def test_yaml_config(self):
        def format(config):
            config['test'] = True
            return config

        print(yamlconfig.load_config_from_yaml(
            """
            repositories:
              ovh: &ovh
                OS_MACHIN: truc
              ovh-grafana:
                <<: *ovh
                OS_MACHIN2: hello ${NAME} !
                OS_ENABLED: ${ENABLED|bool}
                OS_PORT: ${PORT|int}
            """,
            {
                'NAME': 'Frank',
                'PORT': '80',
                'ENABLED': 'True'
            },
            format
        ))


    def test_schedule_once(self):
        def my_action(name):
            if name == 'Paul':
                raise Exception('Bad name')
            print('hello ' + name)

        def on_error(e):
            print('Error handled', e)

        scheduling.schedule_once('1s', my_action, args = ('Jean', ), kwargs={}, on_error =on_error)
        scheduling.schedule_once('1s', my_action, args = ('Paul', ), kwargs={}, on_error =on_error)

        scheduling.schedule_once_in_thread('1s', my_action, args = ('Jean', ), kwargs={}, on_error =on_error)

if __name__ == '__main__':
    unittest.main()

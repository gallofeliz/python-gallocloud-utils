import unittest
import scheduling
import threading
import config
import yamlconfig
import tasks
import logging
import time
import jsonlogging

class TestStringMethods(unittest.TestCase):

    def test_logging(self):
       jsonlogging.configure_logger('INFO').info('main')
       def hello():
            jsonlogging.configure_logger('INFO').info('thread')
       threading.Thread(target=hello).start()

    def test_tasks(self):
        task0 = tasks.Task(lambda: print('exec8'), id='task0', priority='on-idle')
        task1 = tasks.Task(lambda: print('exec4'), id='task1', priority=8)
        task2 = tasks.Task(lambda: print('exec1'), id='task2', priority='immediate')
        task3 = tasks.Task(lambda: print('exec5'), id='task3', priority='normal')
        task4 = tasks.Task(lambda: print('exec7'), id='task4', priority='inferior')
        task5 = tasks.Task(lambda: print('exec6'), id='task5', priority=-16)
        task6 = tasks.Task(lambda: print('exec3'), id='task6', priority='superior')
        task7 = tasks.Task(lambda: print('exec2'), id='task7', priority='next')

        task_manager = tasks.TaskManager(logging)
        task_manager.add_task(task1)
        task_manager.add_task(task2)
        task_manager.add_task(task0)
        task_manager.add_task(task3)
        task_manager.add_task(task4)
        task_manager.add_task(task4, ignore_if_duplicate=False)
        task_manager.add_task(task5)
        task_manager.add_task(task6)
        task_manager.add_task(task7)

        task_manager.run()
        time.sleep(1)
        task_manager.stop()


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
            envs={
                'NAME': 'Frank',
                'PORT': '80',
                'ENABLED': 'True'
            },
            format=format
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

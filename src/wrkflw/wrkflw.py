import logging
import time


class Task:
    def __init__(self, name):
        self.name = name
        self.task = False
        self.status = "init"  # init - waiting - running - finished - failed

    def set_status(self, new_status):
        if new_status in ["init", "waiting", "running", "finished", "failed"]:
            self.status = new_status

    def run(self):
        self.task()


class DummyTask(Task):
    def __init__(self, name):
        super().__init__(name)

    def set_task(self, sleep_seconds):
        def thunk():
            logging.info("Task %s: starting", self.name)
            time.sleep(sleep_seconds)
            logging.info("Task %s: finishing", self.name)
        self.task = thunk


class ShellTask(Task):
    pass


class PythonTask(Task):
    def __init__(self):
        self.task = False

    def set_task(self, fun):
        if callable(fun):
            self.task = fun



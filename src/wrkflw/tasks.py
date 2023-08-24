import os.path
import time
import subprocess
from enum import Enum


class Status(Enum):
    INIT = "init"
    WAITING = "waiting"
    RUNNING = "running"
    FINISHED = "finished"
    FAILED = "failed"


class Task:
    def __init__(self, name):
        self.name = name
        self.task = False
        self.status = Status.INIT

    def get_name(self):
        return self.name

    def reset_status(self):
        self.status = Status.WAITING

    def run(self):
        self.status = Status.RUNNING
        has_succeeded = self.task()
        if has_succeeded:
            self.status = Status.FINISHED
        else:
            self.status = Status.FAILED


class SleepTask(Task):
    def __init__(self, name, seconds = 1):
        super().__init__(name)
        self.set_task(seconds)

    def set_task(self, sleep_seconds):
        super().reset_status()

        def thunk():
            print(f"SleepTask {self.name}: starting")
            time.sleep(sleep_seconds)
            print(f"SleepTask {self.name}: finishing")
            return True

        self.task = thunk


class ShellTask(Task):
    def __init__(self, name):
        super().__init__(name)

    def set_task(self, shell_path):
        if os.path.splitext(shell_path)[1] == ".bat":
            super().reset_status()

            def thunk():
                print(f"ShellTask {self.name}: starting")
                output = subprocess.run(shell_path, shell=True, text=True, capture_output=True)
                last_line = output.stdout.strip().splitlines()[-1]
                has_succeeded = "success" in last_line.lower()
                print(f"ShellTask {self.name}: finishing")
                return has_succeeded

            self.task = thunk


class PythonTask(Task):
    def __init__(self, name):
        super().__init__(name)

    def set_task(self, fun):
        if callable(fun):
            super().reset_status()

            def thunk():
                print(f"ShellTask {self.name}: starting")
                try:
                    fun()
                    has_succeeded = True
                except:
                    has_succeeded = False
                print(f"ShellTask {self.name}: finishing")
                return has_succeeded

            self.task = thunk



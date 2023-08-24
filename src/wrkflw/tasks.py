import os.path
import time
import subprocess

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


class SleepTask(Task):
    def __init__(self, name):
        super().__init__(name)

    def set_task(self, sleep_seconds):
        def thunk():
            print(f"SleepTask {self.name}: starting")
            time.sleep(sleep_seconds)
            print(f"SleepTask {self.name}: finishing")
        self.task = thunk


class ShellTask(Task):
    def __init__(self, name):
        super().__init__(name)

    def set_task(self, shell_path):
        if os.path.splitext(shell_path)[1] == ".bat":
            def thunk():
                print(f"ShellTask {self.name}: starting")
                subprocess.call(shell_path)
                print(f"ShellTask {self.name}: finishing")
            self.task = thunk


class PythonTask(Task):
    def __init__(self, name):
        super().__init__(name)

    def set_task(self, fun):
        if callable(fun):
            def thunk():
                print(f"ShellTask {self.name}: starting")
                fun()
                print(f"ShellTask {self.name}: finishing")
            self.task = thunk



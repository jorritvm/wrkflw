import os.path
import time
import subprocess
from enum import Enum
import tempfile


class Status(Enum):
    INIT = ("Init", "blue")
    WAITING = ("Waiting", "orange")
    RUNNING = ("Running", "yellow")
    FINISHED = ("Finished", "green")
    FAILED = ("Failed", "red")

    def __init__(self, label, color):
        self.label = label
        self.color = color


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
    def __init__(self, name, seconds=1):
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
        self.stderr = ""
        self.stdout = ""
        self.shell_path = ""

    def set_task(self, shell_path):
        super().reset_status()
        self.shell_path = shell_path

        def thunk():
            print(f"ShellTask {self.name}: starting")
            output = subprocess.run(
                shell_path, shell=True, text=True, capture_output=True
            )
            self.stderr = output.stderr
            self.stdout = output.stdout

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


class RTask(Task):
    """
    This class allows the execution of R scripts from within Python.

    Any call to Rscript.exe automatically picks up the renv
    Commandline parameters can be passed to an RScript that is using optparse using a dictionary
    Rscript.exe execution only works if the shell working directory is set to the R project root,
    hence this task creates a temp batch file that takes care of that.
    This batch file is then run as a subprocess.
    If Rscript.exe is not on the PATH you can launch it using its full path

    Attributes:
        batchfile (str): file path of temp batch file
        stdout (str): output from stdout
        stderr (str): output from stderr
    """

    def __init__(self, name):
        super().__init__(name)
        self.stdout = ""
        self.stderr = ""
        self.batchfile = ""

    def set_task(
        self,
        r_file: str,
        parameters: dict,
        rscript_executable: str,
        success_string: str = "success",
        tail_size: int = 5,
        logs_path: str = "",
    ):
        if os.path.splitext(r_file)[1] == ".R":
            super().reset_status()

            # prepare wrapper arguments
            folder, filename = os.path.split(r_file)
            formatted_params_list = [
                f'--{key}="{value}"' for key, value in parameters.items()
            ]
            formatted_params = " ".join(formatted_params_list)

            # write a wrapper batch file
            bat_file_path = self.write_batch_wrapper(
                filename, folder, formatted_params, rscript_executable, logs_path
            )
            self.batchfile = bat_file_path

            # create a python thunk
            def thunk():
                print(f"RTask {self.name}: starting")
                output = subprocess.run(
                    bat_file_path, shell=True, text=True, capture_output=True
                )
                self.write_output(output.stdout, output.stderr)

                print("-------------- caputred job output-----------")
                print(output)
                last_lines = output.stdout.strip().splitlines()[-tail_size:]
                has_succeeded = any(
                    success_string in line.lower() for line in last_lines
                )
                print(f"RTask {self.name}: finishing")
                return has_succeeded

            self.task = thunk

    def write_batch_wrapper(
        self, filename, folder, formatted_params, rscript_executable, logs_path
    ):
        if logs_path == "":
            task_output_folder = tempfile.mkdtemp()
        else:
            task_output_folder = logs_path

        # write a wrapper batch file
        bat_file_content = f"""
            set rscript="{rscript_executable}"
            set "original_dir=%cd%"
            cd /d {folder}
            %rscript% {filename} {formatted_params}
            cd /d "%original_dir%"
            """
        bat_file_path = os.path.join(task_output_folder, "temp_script.bat")
        with open(bat_file_path, "w") as bat_file:
            bat_file.write(bat_file_content)

        return bat_file_path

    def write_output(self, stdout, stderr):
        self.stdout = stdout
        self.stderr = stderr

        output_folder = os.path.dirname(self.batchfile)

        output_stdout = os.path.join(output_folder, "stdout.txt")
        with open(output_stdout, "w") as file:
            file.write(stdout)

        output_stderr = os.path.join(output_folder, "stderr.txt")
        with open(output_stderr, "w") as file:
            file.write(stderr)

import os
import wrkflw as wf
import time

if __name__ == "__main__":
    print(os.getcwd())

    t1 = wf.SleepTask("t1-sleeptask")
    t1.set_task(1)

    t2 = wf.PythonTask("t2-pythontask")
    t2.set_task(lambda: time.sleep(1))

    t3 = wf.ShellTask("t3-shelltask")
    t3.set_task("shell_example.bat")

    t1.run()
    t2.run()
    t3.run()

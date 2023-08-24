import os
import wrkflw as wf
import time

if __name__ == "__main__":
    print(os.getcwd())

    t1 = wf.SleepTask("t1-sleeptask")
    t1.set_task(1)

    t2 = wf.PythonTask("t2-pythontask")
    t2.set_task(lambda: time.sleep(1))

    t2fails = wf.PythonTask("t2-pythontask_that_fails")
    def thunk():
        raise ValueError("This stub fails.")
    t2fails.set_task(thunk)

    t3 = wf.ShellTask("t3-shelltask")
    t3.set_task("shell_example.bat")

    t1.run()

    print(t2.status)
    t2.run()
    print(t2.status)

    print(t2fails.status)
    t2fails.run()
    print(t2fails.status)

    print(t3.status)
    t3.run()
    print(t3.status)

import os
import wrkflw as wf

if __name__ == "__main__":
    print(os.getcwd())

    d1 = wf.DummyTask("dummy1-2sec")
    d1.set_task(2)

    d2 = wf.DummyTask("dummy2-2sec")
    d2.set_task(2)

    d3 = wf.DummyTask("dummy3-4sec")
    d3.set_task(4)

    d4 = wf.DummyTask("dummy4-5sec")
    d4.set_task(5)

    d1.run()
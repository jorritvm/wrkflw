import wrkflw as wf

if __name__ == "__main__":
    t1 = wf.SleepTask('task_1', 1)
    t2 = wf.SleepTask('task_2', 1)
    t3 = wf.SleepTask('task_3', 2)
    t4 = wf.SleepTask('task_4', 1)
    t5 = wf.SleepTask('task_5', 1)
    t6 = wf.PythonTask("pythontask_that_fails")
    def thunk():
        raise ValueError("This stub fails.")
    t6.set_task(thunk)
    t7 = wf.SleepTask('task_7', 1)
    t8 = wf.SleepTask('task_8', 1)

    w = wf.Workflow()
    w.add_relation(t1, t2)
    w.add_relation(t1, t3)
    w.add_relation(t2, t4)
    w.add_relation(t3, t4)
    w.add_relation(t4, t5)
    w.add_relation(t5, t6)
    w.add_relation(t4, t7)
    w.add_relation(t6, t8)
    w.add_relation(t7, t8)

    # t1.run()
    # t2.run()
    # status_table = w.status_table()
    # print(status_table)
    # w.status_viz()

    w.run()
import wrkflw as wf

if __name__ == "__main__":
    t1 = wf.SleepTask('task_1', 1)
    t2 = wf.SleepTask('task_2', 1)
    t3 = wf.SleepTask('task_3', 2)
    t4 = wf.SleepTask('task_4', 1)
    t5 = wf.SleepTask('task_5', 1)

    w = wf.Workflow()
    w.add_edge(t1, t2)
    w.add_edge(t1, t3)
    w.add_edge(t2, t4)
    w.add_edge(t3, t4)
    w.add_edge(t4, t5)

    ts = w.topological_sort()
    print([obj.get_name() for obj in ts])
import wrkflw as wf

if __name__ == "__main__":
    t1 = wf.RTask("r_task_should_succeed")
    t1.set_task(
        r"C:\dev\python\wrkflw\tests\r_sample_code\main.R",
        {"param": "any_value"},
        r"C:\Program Files\R\R-4.2.2\bin\Rscript.exe",
    )
    t2 = wf.RTask("r_task_should_fail")
    t2.set_task(
        r"C:\dev\python\wrkflw\tests\r_sample_code\main.R",
        {"param": "failure"},
        r"C:\Program Files\R\R-4.2.2\bin\Rscript.exe",
    )
    w = wf.Workflow()
    w.add_relation(t1, t2)

    print("-----------start--------------------")
    print(w.status_table())
    t1.run()
    print("-----------t1 ran--------------------")
    print(w.status_table())
    t2.run()
    print("-----------t2 ran--------------------")
    print(w.status_table())
    w.status_viz()

    print("---- showing output of T1---------")
    print("---- T1: stdout---------")
    print(t1.stdout)
    print("---- T1: stderr---------")
    print(t1.stderr)
    print("------logs folder--------")
    print(t1.batchfile)

from elo.cognitive.execution_loop import CognitiveExecutionLoop


class Methods:
    def load(self, context):
        return {"tenant_id": context["tenant_id"], "loss_rate": 0.035}


class Planner:
    def plan(self, task, method, context):
        return ["identify", "calculate", "validate"]


class Executor:
    def execute(self, step, context):
        return {"step": step, "tenant_id": context["tenant_id"]}


class Verifier:
    def verify(self, result, step, method, context):
        return result["tenant_id"] == context["tenant_id"] and bool(method)


class Recorder:
    def __init__(self):
        self.items = []

    def record(self, experience):
        self.items.append(experience)
        return len(self.items)


def test_execution_loop_loads_method_verifies_every_step_and_records():
    recorder = Recorder()
    loop = CognitiveExecutionLoop(Methods(), Planner(), Executor(), Verifier(), recorder)

    trace = loop.run("build budget", tenant_id="tenant-a")

    assert trace.verified == [True, True, True]
    assert trace.experience == 1
    assert recorder.items[0]["tenant_id"] == "tenant-a"


def test_execution_loop_requires_tenant_scope():
    loop = CognitiveExecutionLoop(Methods(), Planner(), Executor(), Verifier(), Recorder())

    try:
        loop.run("task", tenant_id="")
    except ValueError as exc:
        assert "tenant_id" in str(exc)
    else:
        raise AssertionError("missing tenant scope must fail")

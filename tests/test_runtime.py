import pytest
from orco import Builder

def test_runtime_stop(env):
    with env.test_runtime() as runtime:
        runtime.configure_executor(heartbeat_interval=1)
        assert not runtime.stopped

    runtime = env.test_runtime()
    with runtime:
        runtime.configure_executor(heartbeat_interval=1)
        assert not runtime.stopped

    with pytest.raises(Exception):
        with runtime:
            pass


def test_reports(env):
    def adder(config):
        return config["a"] + config["b"]

    runtime = env.test_runtime()
    builder = runtime.register_builder(Builder(adder, "col1"))
    runtime.compute(builder({"a": 10, "b": 30}))

    reports = runtime.get_reports()
    assert len(reports) == 1

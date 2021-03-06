import os
import pickle
import sys

import pytest

TEST_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(TEST_DIR)
sys.path.insert(0, ROOT_DIR)

import orco  # noqa
import logging

logger = logging.getLogger("test")


class TestEnv:

    def __init__(self, tmpdir):
        self.runtimes = []
        self.executors = []
        self.tmpdir = tmpdir
        orco.clear_global_builders()

    def test_runtime(self, **kwargs):
        db_path = str(self.tmpdir.join("db"))
        logger.info("DB path %s", db_path)
        r = orco.Runtime(db_path, **kwargs)
        self.runtimes.append(r)
        return r

    def executor(self, *args, **kwargs):
        executor = orco.internals.executor.Executor(*args, **kwargs)
        self.executors.append(executor)
        return executor

    def file_storage(self, name, init_value):
        return FileStorage(self.tmpdir.join(name), init_value)

    def stop(self):
        for r in self.runtimes:
            if not r.stopped:
                r.stop()
        for e in self.executors:
            if e.runtime:
                e.stop()
        self.runtimes = []
        self.executors = []
        orco.clear_global_builders()


@pytest.fixture()
def env(tmpdir):
    print("Test temp dir", tmpdir)
    test_env = TestEnv(tmpdir)
    orco.clear_global_builders()
    yield test_env
    test_env.stop()


class FileStorage:

    def __init__(self, path, init_value):
        self.path = path
        self.write(init_value)

    def read(self):
        with open(self.path, "rb") as f:
            return pickle.load(f)

    def write(self, count):
        with open(self.path, "wb") as f:
            pickle.dump(count, f)

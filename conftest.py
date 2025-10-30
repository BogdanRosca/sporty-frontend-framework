import yaml
import os
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="prod", help="Environment to run tests against"
    )

@pytest.fixture(scope="session")
def config(request):
    env = request.config.getoption("--env")
    path = os.path.join("config", f"{env}.yaml")
    with open(path) as f:
        data = yaml.safe_load(f)
    return data
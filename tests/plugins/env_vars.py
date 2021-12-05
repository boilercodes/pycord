import os

import pytest


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests():
    os.environ["BOT_TOKEN"] = "ODk3MTVyNDO0MDAxODE0NTC4.YWRgYg.hqWNRy2vEoc8feoNqR0ubBCYwxo"
    os.environ["GUILD_IDS"] = "[776477173123907605,831216309592653835]"

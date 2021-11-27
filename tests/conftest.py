import pytest

from tests import helpers


@pytest.fixture
def hashable_mocks():
    return helpers.MockRole, helpers.MockMember, helpers.MockGuild


@pytest.fixture
def bot():
    return helpers.MockBot()


@pytest.fixture
def ctx():
    return helpers.MockContext()

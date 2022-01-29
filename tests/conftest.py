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


@pytest.fixture
def text_channel():
    return helpers.MockTextChannel()


@pytest.fixture
def id():
    return 297552404041814548  # Randomly generated id.


@pytest.fixture
def content():
    return 297552404041814548  # Randomly generated id.

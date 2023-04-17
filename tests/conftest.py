import pytest
from litestar.testing import create_test_client

from stubborn import Stubborn


@pytest.fixture
def test_client():
    with create_test_client([Stubborn], on_startup=[Stubborn.setup_state]) as client:
        yield client

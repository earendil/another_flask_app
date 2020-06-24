import pytest

from app import create_app

@pytest.fixture(scope='module')
def client():

    test_app = create_app()
    test_client = test_app.test_client()

    context = test_app.app_context()
    context.push()

    yield test_client

    context.pop()
import pytest


@pytest.fixture
def client():
  app = app

  with app.app_context():
    yield app.test_client()
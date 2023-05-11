import flask_testing
from app.config import Config
from app.app import create_app


class TestUserRoutesSimple(flask_testing.TestCase):
    def config(self):
        return Config(testing=True)

    def create_app(self):
        app = create_app(self.config())
        return app

    def test_index_page(self):
        response = self.client.get("/")
        assert response.status_code == 200

    def test_login_page(self):
        response = self.client.get("/login")
        assert response.status_code == 200


# write tests for routes with mocking or databases

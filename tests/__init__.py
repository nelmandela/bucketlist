import json
import unittest

from app import create_app, api, db
from app.views import UserLogin, CreateUser, BucketlistResources
from app.models import Bucketlist, Item, User


class BaseTestCase(unittest.TestCase):
    """Test for API endpoints."""

    def create_app(self):
        app = create_app('testing')
        return app

    def setUp(self):
        """To declare test-wide variables."""

        self.app = self.create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        self.user_credentials = dict(username='dan', password='password123')
        self.user_credentials_2 = dict(username='davy', password='password123')
        self.bucket_1 = dict(name="bucket 1")

        # set api endpoints
        api.add_resource(BucketlistResources, "/api/v1/bucketlists",
                         "/api/v1/bucketlists/<int:id>", endpoint='bucketlist')
        api.add_resource(UserLogin, '/api/v1/auth/login', endpoint="login")
        api.add_resource(CreateUser, '/api/v1/auth/register', endpoint="user_registration")

        # register a user
        self.client.post('/api/v1/auth/register', data=self.user_credentials)
        self.client.post('/api/v1/auth/register', data=self.user_credentials_2)

        self.response = self.client.post('/api/v1/auth/login',
                                         data=self.user_credentials)
        self.response_2 = self.client.post('/api/v1/auth/login',
                                           data=self.user_credentials_2)
        self.response_data_in_json_format = json.loads(
            self.response.data.decode('utf-8'))

        self.response_data_in_json_format_2 = json.loads(
            self.response_2.data.decode('utf-8'))

        # get auth token
        self.token = (self.response_data_in_json_format['Authorization'])
        self.headers = {'Authorization': self.token}

        # token for user 2
        self.token_2 = (self.response_data_in_json_format_2['Authorization'])
        self.headers_2 = {'Authorization': self.token_2}

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


if __name__ == '__main__':
    unittest.main()

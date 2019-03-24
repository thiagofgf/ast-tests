from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_user_register(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username':'Johnson', 'password': '1234'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('Johnson'))
                self.assertEqual(json.loads(response.data), {'message': 'User created successfully'})

    def test_user_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username': 'Johnson', 'password': '1234'})

                auth_response = client.post('/auth',
                                            data=json.dumps({'username': 'Johnson', 'password': '1234'}),
                                            headers={'Content-Type': 'application/json'})

                self.assertIn('access_token',
                              json.loads(auth_response.data).keys())

    def test_user_duplicate(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'Johnson', 'password': '1234'})
                response = client.post('/register',
                                       data=json.dumps({'username': 'Johnson', 'password': '1234'}))

                self.assertEqual(response.status_code, 400)







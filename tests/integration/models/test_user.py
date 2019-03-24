from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            u = UserModel('johnson', '1234')

            self.assertIsNone(UserModel.find_by_username('johnson'))
            self.assertIsNone(UserModel.find_by_id(1))

            u.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username('johnson'))
            self.assertIsNotNone(UserModel.find_by_id(1))

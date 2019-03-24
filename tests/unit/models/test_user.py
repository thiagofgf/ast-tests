from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self):
        u = UserModel('xxx', 'pass')

        self.assertEqual(u.username, 'xxx',
                         'The name of the user after creation does not equal constructor argument')

        self.assertEqual(u.password, 'pass',
                         'The password of the user after creation does not equal constructor argument')

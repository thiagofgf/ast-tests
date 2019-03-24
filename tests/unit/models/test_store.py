from unittest import TestCase
from models.store import StoreModel


class StoreTest(TestCase):
    def test_constructor(self):
        s = StoreModel('Test')

        self.assertEqual(s.name, 'Test')

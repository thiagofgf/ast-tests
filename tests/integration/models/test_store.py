from tests.base_test import BaseTest
from models.item import ItemModel
from models.store import StoreModel


class StoreTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            store = StoreModel('Test')

            self.assertIsNone(store.find_by_name('Test'))

            store.save_to_db()

            self.assertIsNotNone(store.find_by_name('Test'))

            store.delete_from_db()

            self.assertIsNone(store.find_by_name('Test'))

    def test_items_is_empty(self):
        with self.app_context():
            store = StoreModel('Test')

            store.save_to_db()

            self.assertEqual(store.items.count(), 0)

    def test_json(self):
        with self.app_context():
            store = StoreModel('Test')

            store.save_to_db()

            expected = {'name': 'Test', 'items': [], 'id': 1}

            self.assertDictEqual(expected, store.json())

    def test_json_multiple_items(self):
        with self.app_context():
            store = StoreModel('Test')
            item = ItemModel('item', 19.99, 1)
            item2 = ItemModel('item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()
            item2.save_to_db()

            expected = {'name': 'Test', 'id': 1, 'items': [
                {
                    'name': 'item',
                    'price': 19.99
                },
                {
                    'name': 'item',
                    'price': 19.99
                }
            ]}

            self.assertDictEqual(expected, store.json())

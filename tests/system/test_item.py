from models.store import StoreModel
from models.item import ItemModel
from models.user import UserModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()

        with self.app() as client:
            with self.app_context():
                user = UserModel('Jay', '1234')
                user.save_to_db()

                auth_resp = client.post('/auth',
                                        data=json.dumps({'username': 'Jay', 'password': '1234'}),
                                        headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_resp.data)['access_token']
                self.token = f'JWT {auth_token}'

    def test_get_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/Water')

                self.assertEqual(resp.status_code, 401)

    def test_get_no_item(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/Water', headers={'Authorization': self.token})

                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual({'message': 'Item not found'}, json.loads(resp.data))

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('CakeCo')
                store.save_to_db()

                item = ItemModel('Water', 3.00, 1)
                item.save_to_db()

                resp = client.get('/item/Water', headers={'Authorization': self.token})

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'name': 'Water', 'price': 3.00}, json.loads(resp.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('CakeCo')
                store.save_to_db()

                client.post('/item/Water', data={'price': 3.00, 'store_id': 1})
                resp = client.post('/item/Water', data={'price': 3.00, 'store_id': 1})

                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({'message': "An item with name 'Water' already exists."},
                                     json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('CakeCo')
                store.save_to_db()

                resp = client.post('/item/Water', data={'price': 3.00, 'store_id': 1})

                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual(json.loads(resp.data), {'name': 'Water', 'price': 3.00})

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('CakeCo')
                store.save_to_db()

                item = ItemModel('Water', 3.00, 1)
                item.save_to_db()

                resp = client.delete('/item/Water')

                self.assertEqual(resp.status_code, 200)

    def test_update_item_if_exists(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('CakeCo')
                store.save_to_db()

                item = ItemModel('Water', 3.00, 1)
                item.save_to_db()

                self.assertEqual(ItemModel.find_by_name('Water').price, 3.00)

                resp = client.put('/item/Water', data={'price': 4.00, 'store_id': 1})

                self.assertEqual(ItemModel.find_by_name('Water').price, 4.00)
                self.assertDictEqual({'name': 'Water', 'price': 4.00}, json.loads(resp.data))

    def test_create_item_if_not_exists(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('CakeCo')
                store.save_to_db()

                resp = client.put('/item/Water', data={'price': 4.00, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'name': 'Water', 'price': 4.00}, json.loads(resp.data))

    def test_get_items_list(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('CakeCo')
                store.save_to_db()

                item = ItemModel('Water', 3.00, 1)
                item.save_to_db()

                resp = client.get('/items')

                self.assertDictEqual({'items': [{'name': 'Water', 'price': 3.00}]}, json.loads(resp.data))







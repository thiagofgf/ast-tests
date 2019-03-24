from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                resp = client.post('/store/CakeCo')

                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('CakeCo'))
                self.assertDictEqual({'name':'CakeCo','id': 1, 'items':[]}, json.loads(resp.data))

    def test_create_duplicate_sotre(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/CakeCo')
                resp = client.post('/store/CakeCo')

                self.assertEqual(resp.status_code, 400)

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/CakeCo')

                self.assertIsNotNone(StoreModel.find_by_name('CakeCo'))

                resp = client.delete('/store/CakeCo')
                self.assertEqual(resp.status_code, 200)
                self.assertIsNone(StoreModel.find_by_name('CakeCo'))
                self.assertDictEqual({'message': 'Store deleted'},
                                     json.loads(resp.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/CakeCo')

                resp = client.get('/store/CakeCo')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'name':'CakeCo','id': 1, 'items':[]},
                                     json.loads(resp.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/store/CakeCo')

                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'},
                                     json.loads(resp.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                s = StoreModel('CakeCo').save_to_db()
                i = ItemModel('Bolinho', 7.00, 1).save_to_db()

                resp = client.get('/store/CakeCo')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'name': 'CakeCo', 'id': 1,'items': [{'name':'Bolinho','price':7.00}]},
                                     json.loads(resp.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('CakeCo').save_to_db()
                StoreModel('Milho').save_to_db()

                resp = client.get('/stores')
                self.assertDictEqual({'stores': [{'name':'CakeCo','id': 1, 'items': []},
                                                 {'name': 'Milho','id': 2, 'items': []}]},
                                     json.loads(resp.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('CakeCo').save_to_db()
                i = ItemModel('Bolinho', 7.00, 1).save_to_db()
                StoreModel('Milho').save_to_db()
                i = ItemModel('Pamonha', 5.00, 2).save_to_db()

                resp = client.get('/stores')
                self.assertDictEqual({'stores': [{'name':'CakeCo','id': 1, 'items': [{'name':'Bolinho','price':7.00}]},
                                                 {'name': 'Milho','id': 2, 'items': [{'name':'Pamonha','price':5.00}]}]},
                                     json.loads(resp.data))




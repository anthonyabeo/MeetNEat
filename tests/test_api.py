import datetime
import json
import unittest

from mongoengine import connect

from MeetNEat import create_app


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('staging')
        self.db_test = connect('meetneattest')
        self.client = self.app.test_client

        self.request = {
            'meal_type': 'dinner',
            'location': 'Dzorwulu',
            'longitude': 67.76,
            'latitude': 45.86,
            'meal_time': datetime.datetime.now().time(),
            'user_id': 1
        }

        self.proposal = {
            'user_proposed_to': "Sam",
            'user_proposed_from': "Ruby",
            'request_id': 1
        }

        self.meal_date = {
            'user_1': 'Alice',
            'user_2': 'Bob',
            'restaurant_name': 'Kings Place',
            'restaurant_address': '10 Kings Road, Accra',
            'meal_time': datetime.datetime.now().time()
        }

        self.user = {
            'username': "aabeo",
            'password': "encrypted_password"
        }

    # REQUESTS
    # def test_api_can_create_request(self):
    #     res = self.client().post('/api/v1/requests/', data=self.request)
    #     self.assertEqual(res.status_code, 201)
    #     self.assertIn('dinner', str(res.data))
    #
    # def test_api_can_get_all_requests(self):
    #     res = self.client().post('/api/v1/requests/', data=self.request)
    #     self.assertEqual(res.status_code, 201)
    #     res = self.client().get('/api/v1/requests/')
    #     self.assertEqual(res.status_code, 200)
    #     self.assertIn('dinner', str(res.data))
    #
    # def test_api_can_get_a_request(self):
    #     rv = self.client().post('/api/v1/requests/', data=self.request)
    #     self.assertEqual(rv.status_code, 201)
    #     result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
    #     result = self.client().get(
    #         '/api/v1/requests/{}'.format(result_in_json['id']))
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('dinner', str(result.data))
    #
    # def test_api_can_edit_a_request(self):
    #     rv = self.client().post(
    #         '/api/v1/requests/',
    #         data={
    #             'meal_type': 'dinner',
    #             'location': 'Dzorwulu',
    #             'longitude': 67.76,
    #             'latitude': 45.86,
    #             'meal_time': datetime.datetime.now().time(),
    #             'user_id': 1
    #         })
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.client().put(
    #         '/api/v1/requests/1',
    #         data={
    #             "meal_type": "Dessert:-)"
    #         })
    #     self.assertEqual(rv.status_code, 200)
    #     results = self.client().get('/api/v1/requests/1')
    #     self.assertIn('Dessert', str(results.data))
    #
    # def test_api_can_delete_a_request(self):
    #     rv = self.client().post(
    #         '/api/v1/requests/',
    #         data={
    #             'meal_type': 'dinner',
    #             'location': 'Dzorwulu',
    #             'longitude': 67.76,
    #             'latitude': 45.86,
    #             'meal_time': datetime.datetime.now().time(),
    #             'user_id': 1
    #         })
    #     self.assertEqual(rv.status_code, 201)
    #     res = self.client().delete('/api/v1/requests/1')
    #     self.assertEqual(res.status_code, 200)
    #     # Test to see if it exists, should return a 404
    #     result = self.client().get('/api/v1/requests/1')
    #     self.assertEqual(result.status_code, 404)

#     # PROPOSALS
#     def test_api_can_create_proposal(self):
#         res = self.client().post('/api/v1/proposals/', data=self.proposal)
#         self.assertEqual(res.status_code, 201)
#         self.assertIn('Sam', str(res.data))
#
#     def test_api_can_get_all_proposal(self):
#         res = self.client().post('/api/v1/proposals/', data=self.proposal)
#         self.assertEqual(res.status_code, 201)
#         res = self.client().get('/api/v1/proposals/')
#         self.assertEqual(res.status_code, 200)
#         self.assertIn('Sam', str(res.data))
#
#     def test_api_can_get_a_proposal(self):
#         rv = self.client().post('/api/v1/proposals/', data=self.proposal)
#         self.assertEqual(rv.status_code, 201)
#         result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
#         result = self.client().get(
#             '/api/v1/proposals/{}'.format(result_in_json['id']))
#         self.assertEqual(result.status_code, 200)
#         self.assertIn('Sam', str(result.data))
#
#     def test_api_can_edit_a_proposal(self):
#         rv = self.client().post(
#             '/api/v1/proposals/',
#             data={
#                 'user_proposed_to': "Sam",
#                 'user_proposed_from': "Ruby",
#                 'request_id': 1
#             })
#         self.assertEqual(rv.status_code, 201)
#         rv = self.client().put(
#             '/api/v1/proposals/1',
#             data={
#                 "user_proposed_to": "Dennis"
#             })
#         self.assertEqual(rv.status_code, 200)
#         results = self.client().get('/api/v1/proposals/1')
#         self.assertIn('Dennis', str(results.data))
#
#     def test_api_can_delete_a_proposal(self):
#         rv = self.client().post(
#             '/api/v1/proposals/',
#             data={
#                 'user_proposed_to': "Sam",
#                 'user_proposed_from': "Ruby",
#                 'request_id': 1
#             })
#         self.assertEqual(rv.status_code, 201)
#         res = self.client().delete('/api/v1/proposals/1')
#         self.assertEqual(res.status_code, 200)
#         # Test to see if it exists, should return a 404
#         result = self.client().get('/api/v1/proposals/1')
#         self.assertEqual(result.status_code, 404)
#
#     # MEAL DATE
#     def test_api_can_create_meal_date(self):
#         res = self.client().post('/api/v1/dates/', data=self.meal_date)
#         self.assertEqual(res.status_code, 201)
#         self.assertIn('Alice', str(res.data))
#
#     def test_api_can_get_all_meal_date(self):
#         res = self.client().post('/api/v1/dates/', data=self.meal_date)
#         self.assertEqual(res.status_code, 201)
#         res = self.client().get('/api/v1/dates/')
#         self.assertEqual(res.status_code, 200)
#         self.assertIn('Alice', str(res.data))
#
#     def test_api_can_get_a_meal_date(self):
#         rv = self.client().post('/api/v1/dates/', data=self.meal_date)
#         self.assertEqual(rv.status_code, 201)
#         result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
#         result = self.client().get(
#             '/api/v1/dates/{}'.format(result_in_json['id']))
#         self.assertEqual(result.status_code, 200)
#         self.assertIn('Alice', str(result.data))
#
#     def test_api_can_edit_a_meal_date(self):
#         rv = self.client().post(
#             '/api/v1/dates/',
#             data={
#                 'user_1': 'Alice',
#                 'user_2': 'Bob',
#                 'restaurant_name': 'Kings Place',
#                 'restaurant_address': '10 Kings Road, Accra',
#                 'meal_time': datetime.datetime.now().time()
#             })
#         self.assertEqual(rv.status_code, 201)
#         rv = self.client().put(
#             '/api/v1/dates/1',
#             data={
#                 "user_1": "Angela"
#             })
#         self.assertEqual(rv.status_code, 200)
#         results = self.client().get('/api/v1/dates/1')
#         self.assertIn('Angela', str(results.data))
#
#     def test_api_can_delete_a_meal_date(self):
#         rv = self.client().post(
#             '/api/v1/dates/',
#             data={
#                 'user_1': 'Alice',
#                 'user_2': 'Bob',
#                 'restaurant_name': 'Kings Place',
#                 'restaurant_address': '10 Kings Road, Accra',
#                 'meal_time': datetime.datetime.now().time()
#             })
#         self.assertEqual(rv.status_code, 201)
#         res = self.client().delete('/api/v1/dates/1')
#         self.assertEqual(res.status_code, 200)
#         # Test to see if it exists, should return a 404
#         result = self.client().get('/api/v1/dates/1')
#         self.assertEqual(result.status_code, 404)
#

    def test_api_can_create_or_login_user_regular(self):
        res = self.client().post('/api/v1/users/', data=self.user)
        data = json.loads(res.data.decode())

        self.assertEqual(data['status_code'], 201)
        self.assertEqual(data['message'], "User created successfully")
        self.assertIsNotNone(data['username'])

        res = self.client().post('/api/v1/users/', data=self.user)
        data = json.loads(res.data.decode())

        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['message'], "Login successful")
        self.assertIsNotNone(data['token'])
        self.assertIsNotNone(data['id'])

    def test_api_can_get_all_users(self):
        res = self.client().post('/api/v1/users/', data=self.user)
        data = json.loads(res.data.decode())
        self.assertEqual(data['status_code'], 201)
        self.assertEqual(data['message'], "User created successfully")
        self.assertIsNotNone(data['username'])

        res = self.client().post('/api/v1/users/', data=self.user)
        data = json.loads(res.data.decode())
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['message'], "Login successful")
        self.assertIsNotNone(data['token'])

        d = {'token': data['token']}

        res = self.client().get('/api/v1/users/', data=json.dumps(d))
        data = json.loads(res.data.decode())
        self.assertEqual(data['status_code'], 200)
        self.assertIsInstance(data['users'], list)
        self.assertEquals(len(data['users']), 1)

    def test_api_can_get_a_user(self):
        res = self.client().post('/api/v1/users/', data=self.user)
        data = json.loads(res.data.decode())
        self.assertEqual(data['status_code'], 201)
        self.assertEqual(data['message'], "User created successfully")
        self.assertIsNotNone(data['username'])

        res = self.client().post('/api/v1/users/', data=self.user)
        data = json.loads(res.data.decode())
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['message'], "Login successful")
        self.assertIsNotNone(data['token'])

        d = {
            'token': data['token']
        }

        result = self.client().get(
            '/api/v1/users/{}/'.format(data['id']), data=json.dumps(d))

        res = json.loads(result.data.decode())

        self.assertEqual(res['status_code'], 200)
        self.assertIn('aabeo', res['user']['username'])

    def test_api_can_edit_a_user(self):
        res = self.client().post('/api/v1/users/', data=self.user)
        data = json.loads(res.data.decode())
        self.assertEqual(data['status_code'], 201)
        self.assertEqual(data['message'], "User created successfully")
        self.assertIsNotNone(data['username'])

        res = self.client().post('/api/v1/users/', data=self.user)
        data = json.loads(res.data.decode())
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['message'], "Login successful")
        self.assertIsNotNone(data['token'])

        d = {
            'token': data['token'],
            'new_user_info': {
                'username': 'midas',
                'first_name': 'Snow',
                'last_name': '',
                'email': 'midas@midas.com',
                'about_me': 'Carefree since ...'
            }
        }

        rv = self.client().put(
            '/api/v1/users/{}/'.format(data['id']), data=json.dumps(d))
        data = json.loads(rv.data.decode())
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['message'], 'Profile updated successfully')

    def test_api_can_delete_a_user(self):
        res = self.client().post('/api/v1/users/', data=self.user)
        data = json.loads(res.data.decode())

        self.assertEqual(data['status_code'], 201)
        self.assertEqual(data['message'], "User created successfully")
        self.assertIsNotNone(data['username'])

        res = self.client().post('/api/v1/users/', data=self.user)
        data = json.loads(res.data.decode())

        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['message'], "Login successful")
        self.assertIsNotNone(data['token'])
        self.assertIsNotNone(data['id'])

        res = self.client().delete('/api/v1/users/{}/'.format(data['id']), data=json.dumps({'token': data['token']}))
        data = json.loads(res.data.decode())

        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['message'], 'user deleted successfully')

    def tearDown(self):
        self.db_test.drop_database('meetneattest')


if __name__ == '__main__':
    unittest.main()

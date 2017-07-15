import datetime
import json
import unittest

from MeetNEat import create_app, db
from api.models import User, Request, Proposal, MealDate


# class ApiModelsTestCase(unittest.TestCase):
#     """This class tests the Models for API"""
#
#     def setUp(self):
#         self.user = User(username="anthonyabeo",
#                          first_name="Anthony",
#                          last_name="Abeo",
#                          email="anthonyabeo@gmail.com")
#
#         self.request = Request(meal_type='dinner', location='Dzorwulu',
#                                longitude=67.76, latitude=45.86,
#                                meal_time=datetime.datetime.now().time(), user_id=1)
#
#         self.proposal = Proposal(user_proposed_to="Sam",
#                                  user_proposed_from="Ruby",
#                                  request_id=1)
#
#         self.meal_date = MealDate(user_1='Alice', user_2='Bob',
#                              restaurant_name='Kings Place',
#                              restaurant_address='10 Kings Road, Accra',
#                              meal_time=datetime.datetime.now().time())
#
#         self.app = create_app('default')
#         with self.app.app_context():
#             db.create_all()
#
#     # USERS
#     def test_model_can_create_user(self):
#         """verify whether or not a user can be created"""
#
#         old_count = len(User.get_all())
#         self.user.save()
#         new_count = len(User.get_all())
#
#         self.assertNotEqual(old_count, new_count)
#
#     def test_model_can_get_all_users(self):
#         """Verify that all users can be retrieved"""
#
#         self.user.save()
#
#         users = User.get_all()
#         self.assertIsNotNone(users)
#         self.assertIsInstance(users, list)
#         self.assertEqual(len(users), 1)
#
#     def test_model_can_get_a_user(self):
#         """Verify that a user can be retrieved"""
#
#         self.user.save()
#
#         u = User.query.filter_by(username='anthonyabeo').first()
#         self.assertIsNotNone(u)
#         self.assertEqual(u.last_name, 'Abeo')
#
#     def test_model_can_edit_user(self):
#
#         self.user.save()
#
#         old_count = len(User.get_all())
#
#         u = User.query.filter_by(username='anthonyabeo').first()
#         u.email = 'aabeo@gmail.com'
#         u.last_name = 'Newman'
#
#         new_count = len(User.get_all())
#
#         u.save()
#
#         self.assertEqual(u.email, 'aabeo@gmail.com')
#         self.assertEqual(u.last_name, 'Newman')
#         self.assertEqual(old_count, new_count)
#
#     def test_model_can_delete_user(self):
#         """Verify that user can be deleted"""
#
#         self.user.save()
#
#         old_count = len(User.get_all())
#
#         u = User.query.filter_by(username='anthonyabeo').first()
#         User.delete(u)
#
#         new_count = len(User.get_all())
#
#         self.assertNotEqual(old_count, new_count)
#
#         user = User.query.filter_by(username='anthonyabeo').first()
#         self.assertIsNone(user)
#
#     # REQUESTS
#     def test_model_can_create_request(self):
#         """verify whether or not a request can be created"""
#
#         old_count = len(Request.get_all())
#         self.request.save()
#         new_count = len(Request.get_all())
#
#         self.assertNotEqual(old_count, new_count)
#
#     def test_model_can_get_all_requests(self):
#         """Verify that all requests can be retrieved"""
#
#         self.request.save()
#
#         requests = Request.get_all()
#         self.assertIsNotNone(requests)
#         self.assertIsInstance(requests, list)
#         self.assertEqual(len(requests), 1)
#
#     def test_model_can_get_a_request(self):
#         """Verify that a request can be retrieved"""
#
#         self.request.save()
#
#         r = Request.query.filter_by(meal_type='dinner').first()
#         self.assertIsNotNone(r)
#         self.assertEqual(r.location, 'Dzorwulu')
#
#     def test_model_can_edit_request(self):
#         """Verify that a request can be edited"""
#
#         self.request.save()
#
#         old_count = len(Request.get_all())
#
#         r = Request.query.filter_by(meal_type='dinner').first()
#         r.email = 'aabeo@gmail.com'
#         r.last_name = 'Newman'
#
#         new_count = len(Request.get_all())
#
#         r.save()
#
#         self.assertEqual(r.location, 'Dzorwulu')
#         self.assertEqual(r.longitude, 67.76)
#         self.assertEqual(old_count, new_count)
#
#     def test_model_can_delete_request(self):
#         """Verify that a request can be deleted"""
#
#         self.request.save()
#
#         old_count = len(Request.get_all())
#
#         r = Request.query.filter_by(meal_type='dinner').first()
#         Request.delete(r)
#
#         new_count = len(Request.get_all())
#
#         self.assertNotEqual(old_count, new_count)
#
#         r = Request.query.filter_by(meal_type='dinner').first()
#         self.assertIsNone(r)
#
#     # PROPOSALS
#     def test_model_can_create_proposal(self):
#
#         old_count = len(Proposal.get_all())
#         self.proposal.save()
#         new_count = len(Proposal.get_all())
#
#         self.assertNotEqual(old_count, new_count)
#
#     def test_model_can_get_all_proposals(self):
#
#         self.proposal.save()
#
#         p = Proposal.get_all()
#         self.assertIsNotNone(p)
#         self.assertIsInstance(p, list)
#         self.assertEqual(len(p), 1)
#
#     def test_model_can_get_a_proposal(self):
#
#         self.proposal.save()
#
#         p = Proposal.query.filter_by(user_proposed_to='Sam').first()
#         self.assertIsNotNone(p)
#         self.assertEqual(p.user_proposed_from, 'Ruby')
#
#     def test_model_can_edit_proposal(self):
#
#         self.proposal.save()
#
#         old_count = len(Proposal.get_all())
#
#         p = Proposal.query.filter_by(user_proposed_to='Sam').first()
#         p.user_proposed_from = 'Emily'
#
#         new_count = len(Proposal.get_all())
#
#         p.save()
#
#         self.assertEqual(p.user_proposed_from, 'Emily')
#         self.assertEqual(old_count, new_count)
#
#     def test_model_can_delete_proposal(self):
#
#         self.proposal.save()
#
#         old_count = len(Proposal.get_all())
#
#         proposal = Proposal.query.filter_by(user_proposed_to='Sam').first()
#         Proposal.delete(proposal)
#
#         new_count = len(Proposal.get_all())
#
#         self.assertNotEqual(old_count, new_count)
#
#         proposal = Proposal.query.filter_by(user_proposed_to='Sam').first()
#         self.assertIsNone(proposal)
#
#     # MEET DATE
#     def test_model_can_create_meet_date(self):
#
#         old_count = len(MealDate.get_all())
#         self.meal_date.save()
#         new_count = len(MealDate.get_all())
#
#         self.assertNotEqual(old_count, new_count)
#
#     def test_model_can_get_all_meet_dates(self):
#
#         self.meal_date.save()
#
#         meal_date = MealDate.get_all()
#         self.assertIsNotNone(meal_date)
#         self.assertIsInstance(meal_date, list)
#         self.assertEqual(len(meal_date), 1)
#
#     def test_model_can_get_a_meet_date(self):
#
#         self.meal_date.save()
#
#         meal_date = MealDate.query.filter_by(user_1='Alice').first()
#         self.assertIsNotNone(meal_date)
#         self.assertEqual(meal_date.restaurant_name, 'Kings Place')
#
#     def test_model_can_edit_meet_date(self):
#
#         self.meal_date.save()
#
#         old_count = len(MealDate.get_all())
#
#         meal_date = MealDate.query.filter_by(user_1='Alice').first()
#         meal_date.restaurant_name = 'Mama P'
#
#         new_count = len(MealDate.get_all())
#
#         meal_date.save()
#
#         self.assertEqual(meal_date.restaurant_name, 'Mama P')
#         self.assertEqual(old_count, new_count)
#
#     def test_model_can_delete_meet_date(self):
#
#         self.meal_date.save()
#
#         old_count = len(MealDate.get_all())
#
#         meal_date = MealDate.query.filter_by(user_1='Alice').first()
#         MealDate.delete(meal_date)
#
#         new_count = len(MealDate.get_all())
#
#         self.assertNotEqual(old_count, new_count)
#
#         meal_date = MealDate.query.filter_by(user_1='Alice').first()
#         self.assertIsNone(meal_date)
#
#     def tearDown(self):
#         with self.app.app_context():
#             db.session.remove()
#             db.drop_all()


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('default')
        self.client = self.app.test_client
        self.token = None

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

        with self.app.app_context():
            db.create_all()

#     # REQUESTS
#     def test_api_can_create_request(self):
#         res = self.client().post('/api/v1/requests/', data=self.request)
#         self.assertEqual(res.status_code, 201)
#         self.assertIn('dinner', str(res.data))
#
#     def test_api_can_get_all_requests(self):
#         res = self.client().post('/api/v1/requests/', data=self.request)
#         self.assertEqual(res.status_code, 201)
#         res = self.client().get('/api/v1/requests/')
#         self.assertEqual(res.status_code, 200)
#         self.assertIn('dinner', str(res.data))
#
#     def test_api_can_get_a_request(self):
#         rv = self.client().post('/api/v1/requests/', data=self.request)
#         self.assertEqual(rv.status_code, 201)
#         result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
#         result = self.client().get(
#             '/api/v1/requests/{}'.format(result_in_json['id']))
#         self.assertEqual(result.status_code, 200)
#         self.assertIn('dinner', str(result.data))
#
#     def test_api_can_edit_a_request(self):
#         rv = self.client().post(
#             '/api/v1/requests/',
#             data={
#                 'meal_type': 'dinner',
#                 'location': 'Dzorwulu',
#                 'longitude': 67.76,
#                 'latitude': 45.86,
#                 'meal_time': datetime.datetime.now().time(),
#                 'user_id': 1
#             })
#         self.assertEqual(rv.status_code, 201)
#         rv = self.client().put(
#             '/api/v1/requests/1',
#             data={
#                 "meal_type": "Dessert:-)"
#             })
#         self.assertEqual(rv.status_code, 200)
#         results = self.client().get('/api/v1/requests/1')
#         self.assertIn('Dessert', str(results.data))
#
#     def test_api_can_delete_a_request(self):
#         rv = self.client().post(
#             '/api/v1/requests/',
#             data={
#                 'meal_type': 'dinner',
#                 'location': 'Dzorwulu',
#                 'longitude': 67.76,
#                 'latitude': 45.86,
#                 'meal_time': datetime.datetime.now().time(),
#                 'user_id': 1
#             })
#         self.assertEqual(rv.status_code, 201)
#         res = self.client().delete('/api/v1/requests/1')
#         self.assertEqual(res.status_code, 200)
#         # Test to see if it exists, should return a 404
#         result = self.client().get('/api/v1/requests/1')
#         self.assertEqual(result.status_code, 404)
#
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
#     # USERS
#     def test_api_can_create_or_login_user_oauth(self):
#         pass
#
#     def test_api_can_logout_oauth_users(self):
#         pass
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

        d = {
            'token': data['token']
        }

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
                'email': '',
                'about_me': 'Carefree since ...'
            }
        }

        rv = self.client().put(
            '/api/v1/users/1/', data=json.dumps(d))
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

        d = {
            'token': data['token']
        }

        res = self.client().delete('/api/v1/users/1/', data=json.dumps(d))
        data = json.loads(res.data.decode())

        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['message'], 'user deleted successfully')

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()

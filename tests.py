import datetime
import unittest

from MeetNEat import create_app, db
from api.models import User, Request, Proposal, MealDate


class ApiModelsTestCase(unittest.TestCase):
    """This class tests the Models for API"""

    def setUp(self):
        self.app = create_app('default')
        with self.app.app_context():
            db.create_all()

    # USERS
    def test_model_can_create_user(self):
        """verify whether or not a user can be created"""

        user = User(username="anthonyabeo",
                    first_name="Anthony",
                    last_name="Abeo",
                    email="anthonyabeo@gmail.com",
                    password="encrypted_password")

        old_count = len(User.get_all())
        user.save()
        new_count = len(User.get_all())

        self.assertNotEqual(old_count, new_count)

    def test_model_can_get_all_users(self):
        """Verify that all users can be retrieved"""

        user = User(username="anthonyabeo",
                    first_name="Anthony",
                    last_name="Abeo",
                    email="anthonyabeo@gmail.com",
                    password="encrypted_password")

        user.save()

        users = User.get_all()
        self.assertIsNotNone(users)
        self.assertIsInstance(users, list)
        self.assertEqual(len(users), 1)

    def test_model_can_get_a_user(self):
        """Verify that a user can be retrieved"""
        user = User(username="anthonyabeo",
                    first_name="Anthony",
                    last_name="Abeo",
                    email="anthonyabeo@gmail.com",
                    password="encrypted_password")

        user.save()

        user = User.query.filter_by(username='anthonyabeo').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.last_name, 'Abeo')

    def test_model_can_edit_user(self):
        user = User(username="anthonyabeo",
                    first_name="Anthony",
                    last_name="Abeo",
                    email="anthonyabeo@gmail.com",
                    password="encrypted_password")

        user.save()

        old_count = len(User.get_all())

        user = User.query.filter_by(username='anthonyabeo').first()
        user.email = 'aabeo@gmail.com'
        user.last_name = 'Newman'

        new_count = len(User.get_all())

        user.save()

        self.assertEqual(user.email, 'aabeo@gmail.com')
        self.assertEqual(user.last_name, 'Newman')
        self.assertEqual(old_count, new_count)

    def test_model_can_delete_user(self):
        """Verify that user can be deleted"""

        user = User(username="anthonyabeo",
                    first_name="Anthony",
                    last_name="Abeo",
                    email="anthonyabeo@gmail.com",
                    password="encrypted_password")

        user.save()

        old_count = len(User.get_all())

        user = User.query.filter_by(username='anthonyabeo').first()
        User.delete(user)

        new_count = len(User.get_all())

        self.assertNotEqual(old_count, new_count)

        user = User.query.filter_by(username='anthonyabeo').first()
        self.assertIsNone(user)

    # # REQUESTS
    def test_model_can_create_request(self):
        """verify whether or not a request can be created"""

        request = Request(meal_type='dinner', location='Dzorwulu',
                          longitude=67.76, latitude=45.86,
                          meal_time=datetime.datetime.now().time(), user_id=1)

        old_count = len(Request.get_all())
        request.save()
        new_count = len(Request.get_all())

        self.assertNotEqual(old_count, new_count)

    def test_model_can_get_all_requests(self):
        """Verify that all requests can be retrieved"""

        request = Request(meal_type='dinner', location='Dzorwulu',
                          longitude=67.76, latitude=45.86,
                          meal_time=datetime.datetime.now().time(), user_id=1)

        request.save()

        requests = Request.get_all()
        self.assertIsNotNone(requests)
        self.assertIsInstance(requests, list)
        self.assertEqual(len(requests), 1)

    def test_model_can_get_a_request(self):
        """Verify that a request can be retrieved"""

        request = Request(meal_type='dinner', location='Dzorwulu',
                          longitude=67.76, latitude=45.86,
                          meal_time=datetime.datetime.now().time(), user_id=1)

        request.save()

        request = Request.query.filter_by(meal_type='dinner').first()
        self.assertIsNotNone(request)
        self.assertEqual(request.location, 'Dzorwulu')

    def test_model_can_edit_request(self):
        """Verify that a request can be edited"""

        request = Request(meal_type='dinner', location='Dzorwulu',
                          longitude=67.76, latitude=45.86,
                          meal_time=datetime.datetime.now().time(), user_id=1)

        request.save()

        old_count = len(Request.get_all())

        request = Request.query.filter_by(meal_type='dinner').first()
        request.email = 'aabeo@gmail.com'
        request.last_name = 'Newman'

        new_count = len(Request.get_all())

        request.save()

        self.assertEqual(request.location, 'Dzorwulu')
        self.assertEqual(request.longitude, 67.76)
        self.assertEqual(old_count, new_count)

    def test_model_can_delete_request(self):
        """Verify that a request can be deleted"""

        request = Request(meal_type='dinner', location='Dzorwulu',
                          longitude=67.76, latitude=45.86,
                          meal_time=datetime.datetime.now().time(), user_id=1)

        request.save()

        old_count = len(Request.get_all())

        request = Request.query.filter_by(meal_type='dinner').first()
        Request.delete(request)

        new_count = len(Request.get_all())

        self.assertNotEqual(old_count, new_count)

        request = Request.query.filter_by(meal_type='dinner').first()
        self.assertIsNone(request)

    # PROPOSALS
    def test_model_can_create_proposal(self):

        proposal = Proposal(user_proposed_to="Sam",
                            user_proposed_from="Ruby",
                            request_id=1)

        old_count = len(Proposal.get_all())
        proposal.save()
        new_count = len(Proposal.get_all())

        self.assertNotEqual(old_count, new_count)

    def test_model_can_get_all_proposals(self):
        proposal = Proposal(user_proposed_to="Sam",
                            user_proposed_from="Ruby",
                            request_id=1)

        proposal.save()

        proposal = Proposal.get_all()
        self.assertIsNotNone(proposal)
        self.assertIsInstance(proposal, list)
        self.assertEqual(len(proposal), 1)

    def test_model_can_get_a_proposal(self):

        proposal = Proposal(user_proposed_to="Sam",
                            user_proposed_from="Ruby",
                            request_id=1)

        proposal.save()

        proposal = Proposal.query.filter_by(user_proposed_to='Sam').first()
        self.assertIsNotNone(proposal)
        self.assertEqual(proposal.user_proposed_from, 'Ruby')

    def test_model_can_edit_proposal(self):

        proposal = Proposal(user_proposed_to="Sam",
                            user_proposed_from="Ruby",
                            request_id=1)

        proposal.save()

        old_count = len(Proposal.get_all())

        proposal = Proposal.query.filter_by(user_proposed_to='Sam').first()
        proposal.user_proposed_from = 'Emily'

        new_count = len(Proposal.get_all())

        proposal.save()

        self.assertEqual(proposal.user_proposed_from, 'Emily')
        self.assertEqual(old_count, new_count)

    def test_model_can_delete_proposal(self):

        proposal = Proposal(user_proposed_to="Sam",
                            user_proposed_from="Ruby",
                            request_id=1)

        proposal.save()

        old_count = len(Proposal.get_all())

        proposal = Proposal.query.filter_by(user_proposed_to='Sam').first()
        Proposal.delete(proposal)

        new_count = len(Proposal.get_all())

        self.assertNotEqual(old_count, new_count)

        proposal = Proposal.query.filter_by(user_proposed_to='Sam').first()
        self.assertIsNone(proposal)

    # MEET DATE
    def test_model_can_create_meet_date(self):
        meal_date = MealDate(user_1='Alice', user_2='Bob',
                             restaurant_name='Kings Place',
                             restaurant_address='10 Kings Road, Accra',
                             meal_time=datetime.datetime.now().time())

        old_count = len(MealDate.get_all())
        meal_date.save()
        new_count = len(MealDate.get_all())

        self.assertNotEqual(old_count, new_count)

    def test_model_can_get_all_meet_dates(self):

        meal_date = MealDate(user_1='Alice', user_2='Bob',
                             restaurant_name='Kings Place',
                             restaurant_address='10 Kings Road, Accra',
                             meal_time=datetime.datetime.now().time())

        meal_date.save()

        meal_date = MealDate.get_all()
        self.assertIsNotNone(meal_date)
        self.assertIsInstance(meal_date, list)
        self.assertEqual(len(meal_date), 1)

    def test_model_can_get_a_meet_date(self):

        meal_date = MealDate(user_1='Alice', user_2='Bob',
                             restaurant_name='Kings Place',
                             restaurant_address='10 Kings Road, Accra',
                             meal_time=datetime.datetime.now().time())

        meal_date.save()

        meal_date = MealDate.query.filter_by(user_1='Alice').first()
        self.assertIsNotNone(meal_date)
        self.assertEqual(meal_date.restaurant_name, 'Kings Place')

    def test_model_can_edit_meet_date(self):

        meal_date = MealDate(user_1='Alice', user_2='Bob',
                             restaurant_name='Kings Place',
                             restaurant_address='10 Kings Road, Accra',
                             meal_time=datetime.datetime.now().time())

        meal_date.save()

        old_count = len(MealDate.get_all())

        meal_date = MealDate.query.filter_by(user_1='Alice').first()
        meal_date.restaurant_name = 'Mama P'

        new_count = len(MealDate.get_all())

        meal_date.save()

        self.assertEqual(meal_date.restaurant_name, 'Mama P')
        self.assertEqual(old_count, new_count)

    def test_model_can_delete_meet_date(self):

        meal_date = MealDate(user_1='Alice', user_2='Bob',
                             restaurant_name='Kings Place',
                             restaurant_address='10 Kings Road, Accra',
                             meal_time=datetime.datetime.now().time())

        meal_date.save()

        old_count = len(MealDate.get_all())

        meal_date = MealDate.query.filter_by(user_1='Alice').first()
        MealDate.delete(meal_date)

        new_count = len(MealDate.get_all())

        self.assertNotEqual(old_count, new_count)

        meal_date = MealDate.query.filter_by(user_1='Alice').first()
        self.assertIsNone(meal_date)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

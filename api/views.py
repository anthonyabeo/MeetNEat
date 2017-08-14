import json
from datetime import datetime

import foursquare
from bson import ObjectId
from flask import session, request, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal
from MeetNEat.config import FOURSQUARE_CREDENTIALS
from mongoengine import Q

from api import api_blueprint
from api.models import User, Request, Proposal, MealDate
from api.oauth import OAuthSignIn
from api.rate_limit import get_view_rate_limit, ratelimit
from api.utils import verify_credentials

api = Api(api_blueprint)

user_fields = {
    'id': fields.String,
    'username': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'about_me': fields.String
}

request_fields = {
    'id': fields.String,
    'meal_type': fields.String,
    'location_string': fields.String,
    'meal_time': fields.String,
    'created': fields.DateTime,
    'modified': fields.DateTime,
    'filled': fields.Boolean,
    'user': fields.Nested(user_fields)
}

proposal_fields = {
    'id': fields.String,
    'proposal_host': fields.Nested(user_fields),
    'proposal_guest': fields.Nested(user_fields),
    'filled': fields.Boolean,
    'request': fields.Nested(request_fields),
}

md_fields = {
    'id': fields.String,
    'user_1': fields.Nested(user_fields),
    'user_2': fields.Nested(user_fields),
    'longitude': fields.Float,
    'latitude': fields.Float,
    'restaurant_name': fields.String,
    'restaurant_address': fields.String,
    'restaurant_picture': fields.Raw,
    'meal_time': fields.String
}


@api_blueprint.after_request
def inject_x_rate_headers(response):
    limit = get_view_rate_limit()
    if limit and limit.send_x_headers:
        h = response.headers
        h.add('X-RateLimit-Remaining', str(limit.remaining))
        h.add('X-RateLimit-Limit', str(limit.limit))
        h.add('X-RateLimit-Reset', str(limit.reset))
    return response


@api_blueprint.route('/api/v1/authorize/<provider>/login')
def oauth_authorize(provider):
    if 'token' in session:
        user = User.confirm_auth_token(session['token'])
        if user is None:
            session.clear()
            return jsonify({'status_code': 304, 'message': 'Session expired. Kindly log in.'})
        return jsonify({'status_code': 304, 'message': 'Already logged in'})
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@api_blueprint.route('/api/v1/callback/<provider>')
def oauth_callback(provider):
    if 'token' in session:
        user = User.confirm_auth_token(session['token'])
        if user is None:
            session.clear()
            return jsonify({'status_code': 304, 'message': 'Session expired. Kindly log in.'})
        return jsonify({'status_code': 304, 'message': 'Already logged in'})
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        return jsonify({'status_code': 401, 'message': 'Authentication failed'})
    user = User.objects(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, username=username, email=email)
        user.save()

    session['id'] = str(user.id)
    session['username'] = user.username
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    session['email'] = user.email
    session['about_me'] = user.about_me
    session['token'] = user.generate_confirmation_token().decode('ascii')

    return jsonify({
        'status_code': 200,
        'message': 'Successfully logged in',
        'user': {
            'id': session['id'],
            'username': session['username'],
            'first_name': session['first_name'],
            'last_name': session['last_name'],
            'email': session['email'],
            'about_me': session['about_me'],
            'token': session['token']
        }
    })


@api_blueprint.route('/api/v1/users/logout')
def logout_user():
    if session['username']:
        session.clear()
        return jsonify({'message': 'Successfully logged out', 'status_code': 200})
    else:
        return jsonify({'message': 'Already logged out', 'status_code': 200})


# USERS
class UserListApi(Resource):
    decorators = [ratelimit(limit=300, per=30 * 1)]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("username", type=str, help='Username is required', required=True)
        self.parser.add_argument("password", type=str, help='password is required', required=True)
        self.parser.add_argument("email", type=str)

        super(UserListApi, self).__init__()

    def get(self):
        token = request.args.get('token')

        if token:
            user = User.confirm_auth_token(token)
            if user:
                users = User.objects()
                return {
                    'status_code': 200,
                    'users': [marshal(user, user_fields) for user in users]
                }
            else:
                return {'status_code': 401, 'message': 'Invalid credentials!!!'}
        else:
            return {'status_code': 401, 'message': 'You need to login'}

    def post(self):
        args = self.parser.parse_args()
        username = args['username']
        password = args['password']
        email = args['email']

        user = User.objects(username=username).first()

        if user is None:
            user = User(username=username, email=email)
            user.hash_password(password)
            user.save()

            response = {
                'username': user.username,
                'status_code': 201,
                'message': "User created successfully"
            }
            return response
        else:
            if verify_credentials(username, password):

                session['id'] = str(user.id)
                session['username'] = user.username
                session['first_name'] = user.first_name
                session['last_name'] = user.last_name
                session['email'] = user.email
                session['about_me'] = user.about_me
                session['token'] = user.generate_confirmation_token().decode('ascii')

                return {
                    'status_code': 200,
                    'message': 'Successfully logged in',
                    'user': {
                        'id': session['id'],
                        'username': session['username'],
                        'first_name': session['first_name'],
                        'last_name': session['last_name'],
                        'email': session['email'],
                        'about_me': session['about_me'],
                        'token': session['token']
                    }
                }
            else:
                return {'error': 'Invalid credentials. You need to log in'}


class UserApi(Resource):
    decorators = [ratelimit(limit=300, per=30 * 1)]

    def get(self, user_id):

        token = request.args.get('token')

        if token:
            user = User.confirm_auth_token(token)
            if user:
                if str(user.id) == user_id:
                    return {'status_code': 200, 'user': marshal(user, user_fields)}
            else:
                return {'status_code': 404, 'error': 'Invalid credentials!!!'}
        else:
            return {'status_code': 400, 'message': 'You need to login'}

    def put(self, user_id):

        token = request.args.get('token')
        data = json.loads(request.get_data().decode('ascii'))

        new_user_info = data['new_user_info']

        if token:
            user = User.confirm_auth_token(token)
            if user:
                if str(user.id) == user_id:
                    user.username = new_user_info['username']
                    user.first_name = new_user_info['first_name']
                    user.last_name = new_user_info['last_name']
                    user.email = new_user_info['email']
                    user.about_me = new_user_info['about_me']

                    user.save()

                    return {'status_code': 200, 'message': 'Profile updated successfully'}
            else:
                return {'status_code': 404, 'error': 'Invalid credentials!!!'}
        else:
            return {'status_code': 400, 'message': 'You need to login'}

    def delete(self, user_id):

        token = request.args.get('token')

        if token:
            user = User.confirm_auth_token(token)
            if user:
                if str(user.id) == user_id:
                    user.delete()

                    return {'status_code': 200, 'message': 'user deleted successfully'}
            else:
                return {'status_code': 404, 'error': 'Invalid credentials!!!'}
        else:
            return {'status_code': 400, 'message': 'You need to login'}


api.add_resource(UserListApi, '/api/v1/users', endpoint='users')
api.add_resource(UserApi, '/api/v1/users/<string:user_id>', endpoint='user')


# REQUESTS
class RequestListApi(Resource):
    decorators = [ratelimit(limit=300, per=30 * 1)]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("meal_type", type=str, help='Meal Type is required', required=True)
        self.parser.add_argument("location_string", type=str, help='Location is required', required=True)
        self.parser.add_argument("meal_time", type=str, help='Meal time is required', required=True)
        self.parser.add_argument("user", type=str, help='user ID is required', required=True)
        self.parser.add_argument("created", type=object)
        self.parser.add_argument("modified", type=object)
        self.parser.add_argument("filled", type=bool)

        super(RequestListApi, self).__init__()

    def get(self):
        token = request.args.get('token')
        u = request.args.get('user')

        if token:
            user = User.confirm_auth_token(token)
            if user:
                if u == 'me':
                    requests = Request.objects(user__ne=ObjectId(user.id))
                    return {
                        'status_code': 200,
                        'requests': [marshal(req, request_fields) for req in requests]
                    }
                elif u == 'all':
                    requests = Request.objects()
                    return {
                        'status_code': 200,
                        'requests': [marshal(req, request_fields) for req in requests]
                    }
                else:
                    return {'status_code': 401, 'message': 'Provide the USER parameter.'}
            else:
                return {'status_code': 401, 'message': 'Invalid credentials!!!'}
        else:
            return {'status_code': 401, 'message': 'You need to login'}

    def post(self):
        token = request.args.get('token')

        if token:
            user = User.confirm_auth_token(token)
            if user:
                args = self.parser.parse_args()
                meal_type = args['meal_type']
                location_string = args['location_string']
                meal_time = args['meal_time']
                user = args['user']

                req = Request(meal_time=meal_time, meal_type=meal_type,
                              location_string=location_string, user=user)

                req.save()

                return {
                    'status_code': 201,
                    'message': 'Request placed successfully'
                }
            else:
                return {'status_code': 401, 'message': 'Invalid credentials!!!'}
        else:
            return {'status_code': 401, 'message': 'You need to login'}


class RequestApi(Resource):
    decorators = [ratelimit(limit=300, per=30 * 1)]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("meal_type", type=str, help='Meal Type is required', required=True)
        self.parser.add_argument("location_string", type=str, help='Location is required', required=True)
        self.parser.add_argument("meal_time", type=str, help='Meal time is required', required=True)
        self.parser.add_argument("user", type=str, help='user ID is required', required=True)
        self.parser.add_argument("filled", type=bool)

        super(RequestApi, self).__init__()

    def get(self, r_id):
        token = request.args.get('token')
        if token:
            user = User.confirm_auth_token(token)
            if user:
                req = Request.objects(id=r_id).first()
                return {
                    'status_code': 200,
                    'requests': marshal(req, request_fields)
                }
            else:
                return {'status_code': 401, 'message': 'Invalid credentials!!!'}
        else:
            return {'status_code': 401, 'message': 'You need to login'}

    def put(self, r_id):
        token = request.args.get('token')
        if token:
            user = User.confirm_auth_token(token)
            if user:
                args = self.parser.parse_args()

                r = Request.objects.get(id=r_id)
                r.meal_type = args['meal_type']
                r.location_string = args['location_string']
                r.meal_time = args['meal_time']
                r.filled = args['filled']
                r.modified = datetime.now()

                r.save()

                return {'status_code': 200, 'message': 'Request updated'}
            else:
                return {'status_code': 401, 'message': 'Invalid credentials!!!'}
        else:
            return {'status_code': 401, 'message': 'You need to login'}

    def delete(self, r_id):

        token = request.args.get('token')

        if token:
            user = User.confirm_auth_token(token)
            if user:
                    r = Request.objects.get(id=r_id)
                    r.delete()

                    return {'status_code': 204, 'message': 'Request deleted successfully'}
            else:
                return {'status_code': 401, 'error': 'Invalid credentials!!!'}
        else:
            return {'status_code': 401, 'message': 'You need to login'}

api.add_resource(RequestListApi, '/api/v1/requests', endpoint='requests')
api.add_resource(RequestApi, '/api/v1/requests/<string:r_id>', endpoint='request')


# PROPOSALS
class ProposalListApi(Resource):
    decorators = [ratelimit(limit=300, per=30 * 1)]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("proposal_guest", type=str, help='Request guest is required', required=True)
        self.parser.add_argument("request", type=str, required=True)
        self.parser.add_argument("filled", type=bool, required=True)

        super(ProposalListApi, self).__init__()

    def get(self):
        token = request.args.get('token')
        if token:
            user = User.confirm_auth_token(token)
            if user:
                proposals = Proposal.objects(Q(proposal_host=ObjectId(user.id))
                                             | Q(proposal_guest=ObjectId(user.id)))
                return {
                    'status_code': 200,
                    'requests': [marshal(prop, proposal_fields) for prop in proposals]
                }
            else:
                return {'status_code': 401, 'message': 'Invalid credentials!!!'}
        else:
            return {'status_code': 401, 'message': 'You need to login'}

    def post(self):
        token = request.args.get('token')
        if token:
            user = User.confirm_auth_token(token)
            if user:
                args = self.parser.parse_args()
                proposal_guest = args['proposal_guest']
                filled = args['filled']
                req = args['request']

                m_request = Request.objects.get(id=req)
                if m_request:
                    proposal_host = str(m_request.user.id)
                    if proposal_host != proposal_guest:
                        prop = Proposal.objects(request=req)
                        if not prop:
                            proposal = Proposal(proposal_host=proposal_host,
                                                proposal_guest=proposal_guest,
                                                filled=filled,
                                                request=req)
                            proposal.save()

                            return {'status_code': 201, 'message': 'Proposal placed successfully'}
                        else:
                            return {'status_code': 406, 'message': 'Request is already occupied'}
                    else:
                        return {'status_code': 406, 'message': 'Cannot meet with yourself'}
                else:
                    return {'status_code': 406, 'message': 'Request no longer open'}
            else:
                return {'status_code': 401, 'message': 'Invalid credentials!!!'}
        else:
            return {'status_code': 401, 'message': 'You need to login'}


class ProposalApi(Resource):
    decorators = [ratelimit(limit=300, per=30 * 1)]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("proposal_host", type=str, help='Request host is required', required=True)
        self.parser.add_argument("proposal_guest", type=str, help='Request guest is required', required=True)
        self.parser.add_argument("request", type=str, required=True)
        self.parser.add_argument("filled", type=bool, required=True)

        super(ProposalApi, self).__init__()

    def get(self, prop_id):
        token = request.args.get('token')
        if token:
            user = User.confirm_auth_token(token)
            if user:
                prop = Proposal.objects.get(id=prop_id)
                if user.id == prop.proposal_host.id or user.id == prop.proposal_guest.id:
                    return {
                        'status_code': 200,
                        'proposals': marshal(prop, proposal_fields)
                    }
                else:
                    return {'status_code': 401, 'message': 'This proposal is not your concern.'}
            else:
                return {'status_code': 401, 'message': 'Invalid credentials!!!'}
        else:
            return {'status_code': 401, 'message': 'You need to login'}

    def put(self, prop_id):
        token = request.args.get('token')
        if token:
            user = User.confirm_auth_token(token)
            if user:
                args = self.parser.parse_args()

                p = Proposal.objects.get(id=prop_id)

                if p.proposal_host.id == user.id:
                    p.proposal_host = ObjectId(args['proposal_host'])
                    p.proposal_guest = ObjectId(args['proposal_guest'])
                    p.filled = args['filled']
                    p.req = ObjectId(args['request'])

                    p.save()

                    return {
                        'status_code': 200,
                        'message': 'Proposal updated'
                    }
                else:
                    return {'status_code': 401, 'message': 'You cannot edit this proposal. You are did not create it'}
            else:
                return {'status_code': 401, 'message': 'Invalid credentials!!!'}
        else:
            return {'status_code': 401, 'message': 'You need to login'}

    def delete(self, prop_id):
        token = request.args.get('token')
        if token:
            user = User.confirm_auth_token(token)
            if user:
                p = Proposal.objects.get(id=prop_id)
                if p.proposal_host.id == user.id:
                    p.delete()

                    return {
                        'status_code': 204,
                        'message': 'Proposal deleted successfully'
                    }
                else:
                    return {'status_code': 401, 'message': 'cannot delete proposal. You did not create it.'}
            else:
                return {'status_code': 401, 'error': 'Invalid credentials!!!'}
        else:
            return {'status_code': 401, 'message': 'You need to login'}


api.add_resource(ProposalListApi, '/api/v1/proposals', endpoint='proposals')
api.add_resource(ProposalApi, '/api/v1/proposals/<string:prop_id>', endpoint='proposal')


# MEAL DATES
class MealDateListApi(Resource):
    decorators = [ratelimit(limit=300, per=30 * 1)]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("proposal", type=str, help='Proposal required', required=True)

        super(MealDateListApi, self).__init__()

    def get(self):
        token = request.args.get('token')
        if token:
            user = User.confirm_auth_token(token)
            if user:
                mealdates = MealDate.objects(Q(user_1=ObjectId(user.id))
                                             | Q(user_2=ObjectId(user.id)))
                return {
                    'status_code': 200,
                    'mealdates': [marshal(md, md_fields) for md in mealdates]
                }
            else:
                return {'status_code': 401, 'message': 'Invalid credentials!!!'}
        else:
            return {'status_code': 401, 'message': 'You need to login'}

    def post(self):
        token = request.args.get('token')
        decision = request.args.get('decision')

        if token:
            user = User.confirm_auth_token(token)
            if user:
                args = self.parser.parse_args()
                proposal = args['proposal']

                if decision == 'true':
                    p = Proposal.objects.get(id=proposal)
                    req = p.request
                    # use location_string with foursquare to find restaurants
                    client = foursquare.Foursquare(client_id=FOURSQUARE_CREDENTIALS['CLIENT_ID'],
                                                   client_secret=FOURSQUARE_CREDENTIALS['CLIENT_SECRET'])
                    response = client.venues.search(params={'near': req.location_string, 'query': req.meal_type,
                                                            'intent': 'checkin', 'limit': 5})

                    restaurants = response['venues'][0]

                    # store the GPS coordinates and restaurant info
                    # use gps coordinates with G-maps to show map
                    md = MealDate(user_1=p.proposal_host, user_2=p.proposal_guest, proposal=proposal,
                                  restaurant_name=restaurants['name'],
                                  restaurant_address=', '.join(restaurants['location']['formattedAddress']),
                                  latitude=restaurants['location']['lat'], longitude=restaurants['location']['lng'],
                                  meal_time=req.meal_time)
                    md.save()

                    return {
                        'status_code': 201,
                        'message': 'Meal date placed successfully'
                    }
                elif decision == 'false':
                    Proposal.objects.get(id=proposal).delete()
                    return {'status_code': 204, 'message': 'Date cancelled'}
                elif decision == '':
                    return {'status_code': 401, 'message': 'Missing parameter, DECISION'}
            else:
                return {'status_code': 401, 'message': 'Invalid credentials!!!'}
        else:
            return {'status_code': 401, 'message': 'You need to login'}


class MealDateApi(Resource):
    decorators = [ratelimit(limit=300, per=30 * 1)]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("user_1", type=str, help='User 1 required', required=True)
        self.parser.add_argument("user_2", type=str, help='User 2 is required', required=True)
        self.parser.add_argument("restaurant_name", type=str, required=True)
        self.parser.add_argument("restaurant_address", type=str, required=True)
        self.parser.add_argument("restaurant_picture", type=str)
        self.parser.add_argument("meal_time", type=str, required=True)

        super(MealDateApi, self).__init__()

    def get(self, date_id):
        token = request.args.get('token')
        if token:
            user = User.confirm_auth_token(token)
            if user:
                md = MealDate.objects.get(id=date_id)
                return {
                    'status_code': 200,
                    'mealdates': marshal(md, md_fields)
                }
            else:
                return {'status_code': 401, 'message': 'Invalid credentials!!!'}
        else:
            return {'status_code': 401, 'message': 'You need to login'}

    def put(self, date_id):
        token = request.args.get('token')
        if token:
            user = User.confirm_auth_token(token)
            if user:
                args = self.parser.parse_args()

                md = MealDate.objects.get(id=date_id)

                if user.id == md.user_1 or user.id == md.user_2:
                    md.user_1 = ObjectId(args['user_1'])
                    md.user_2 = ObjectId(args['user_2'])
                    md.restaurant_name = args['restaurant_name']
                    md.restaurant_address = args['restaurant_address']
                    md.meal_time = args['meal_time']

                    md.save()

                    return {
                        'status_code': 200,
                        'message': 'Meal date updated'
                    }
                else:
                    return {'status_code': 401, 'message': 'You cannot modify this date info'}
            else:
                return {'status_code': 401, 'message': 'Invalid credentials!!!'}
        else:
            return {'status_code': 401, 'message': 'You need to login'}

    def delete(self, date_id):
        token = request.args.get('token')
        if token:
            user = User.confirm_auth_token(token)
            if user:
                md = MealDate.objects.get(id=date_id)
                if user.id == md.user_1 or user.id == md.user_2:
                    md.delete()

                    return {
                        'status_code': 204,
                        'message': 'Meal date cancelled successfully'
                    }
                else:
                    return {'status_code': 401, 'error': 'Cannot delete date info. You are not involved'}
            else:
                return {'status_code': 401, 'error': 'Invalid credentials!!!'}
        else:
            return {'status_code': 401, 'message': 'You need to login'}

api.add_resource(MealDateListApi, '/api/v1/mealdate', endpoint='mealdates')
api.add_resource(MealDateApi, '/api/v1/mealdate/<string:date_id>', endpoint='mealdate')
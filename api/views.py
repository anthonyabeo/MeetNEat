import json

from bson import ObjectId
from flask import session, request, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal

from api import api_blueprint
from api.models import User, Request, Proposal
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
    'longitude': fields.Float,
    'latitude': fields.Float,
    'meal_time': fields.String,
    'created': fields.DateTime,
    'modified': fields.DateTime,
    'filled': fields.Boolean,
    'user': fields.Nested(user_fields)
}

proposal_fields = {
    'id': fields.String,
    'user_proposed_to': fields.Nested(user_fields),
    'user_proposed_from': fields.Nested(user_fields),
    'filled': fields.Boolean,
    'request': fields.Nested(request_fields),
}


@api_blueprint.route('/api/v1/users/logout')
def logout_user():
    if session['username']:
        session.clear()
    return jsonify({'message': 'Successfully logged out', 'status_code': 200})


class UserListApi(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("username", type=str,
                                 help='Username is required',
                                 required=True)

        self.parser.add_argument("password",
                                 type=str,
                                 help='password is required',
                                 required=True)

        super(UserListApi, self).__init__()

    def get(self):

        data = json.loads(request.get_data().decode('ascii'))
        token = data['token']

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

        user = User.objects(username=username).first()

        if user is None:
            user = User(username=username)
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

                response = {
                    'status_code': 200,
                    'id': session['id'],
                    'message': "Login successful",
                    'token': session['token']
                }
                return response
            else:
                return {'error': 'Invalid credentials!!!'}


class UserApi(Resource):

    def get(self, user_id):

        data = json.loads(request.get_data().decode('ascii'))
        token = data['token']

        if token:
            user = User.confirm_auth_token(token)
            if user:
                if str(user.id) == user_id:
                    return {
                        'status_code': 200,
                        'user': marshal(user, user_fields)
                    }
            else:
                return {
                    'status_code': 404,
                    'error': 'Invalid credentials!!!'
                }
        else:
            return {
                'status_code': 400,
                'message': 'You need to login'
            }

    def put(self, user_id):

        data = json.loads(request.get_data().decode('ascii'))
        token = data['token']
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

                    response = {
                        'status_code': 200,
                        'message': 'Profile updated successfully'
                    }
                    return response
            else:
                return {
                    'status_code': 404,
                    'error': 'Invalid credentials!!!'
                }
        else:
            return {
                'status_code': 400,
                'message': 'You need to login'
            }

    def delete(self, user_id):

        data = json.loads(request.get_data().decode('ascii'))
        token = data['token']

        if token:
            user = User.confirm_auth_token(token)
            if user:
                if str(user.id) == user_id:
                    user.delete()

                    return {
                        'status_code': 200,
                        'message': 'user deleted successfully'
                    }
            else:
                return {
                    'status_code': 404,
                    'error': 'Invalid credentials!!!'
                }
        else:
            return {
                'status_code': 400,
                'message': 'You need to login'
            }


api.add_resource(UserListApi, '/api/v1/users', endpoint='users')
api.add_resource(UserApi, '/api/v1/users/<string:user_id>', endpoint='user')


class RequestListApi(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("meal_type", type=str,
                                 help='Meal Type is required',
                                 required=True)

        self.parser.add_argument("location_string",
                                 type=str,
                                 help='Location is required',
                                 required=True)

        self.parser.add_argument("longitude",
                                 type=float)

        self.parser.add_argument("latitude",
                                 type=float)

        self.parser.add_argument("meal_time",
                                 type=str,
                                 help='Meal time is required',
                                 required=True)

        self.parser.add_argument("user",
                                 type=str,
                                 help='user ID is required',
                                 required=True)

        self.parser.add_argument("created",
                                 type=object)

        self.parser.add_argument("modified",
                                 type=object)

        self.parser.add_argument("filled",
                                 type=bool)

        super(RequestListApi, self).__init__()

    def get(self):
        token = request.args.get('token')
        if token:
            user = User.confirm_auth_token(token)
            if user:
                requests = Request.objects()
                return {
                    'status_code': 200,
                    'requests': [marshal(req, request_fields) for req in requests]
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

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("meal_type", type=str,
                                 help='Meal Type is required',
                                 required=True)

        self.parser.add_argument("location_string",
                                 type=str,
                                 help='Location is required',
                                 required=True)

        self.parser.add_argument("longitude",
                                 type=float)

        self.parser.add_argument("latitude",
                                 type=float)

        self.parser.add_argument("meal_time",
                                 type=str,
                                 help='Meal time is required',
                                 required=True)

        self.parser.add_argument("user",
                                 type=str,
                                 help='user ID is required')

        self.parser.add_argument("created",
                                 type=object)

        self.parser.add_argument("modified",
                                 type=object)

        self.parser.add_argument("filled",
                                 type=bool)

        super(RequestApi, self).__init__()

    def get(self, r_id):
        token = request.args.get('token')
        if token:
            user = User.confirm_auth_token(token)
            if user:
                req = Request.objects.get(id=r_id)
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
                r.user = ObjectId(args['user'])
                r.filled = args['filled']
                r.created = args['created']
                r.modified = args['modified']
                r.longitude = args['longitude']
                r.latitude = args['latitude']

                r.save()

                return {
                    'status_code': 200,
                    'message': 'Request updated'
                }
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

                    return {
                        'status_code': 204,
                        'message': 'Request deleted successfully'
                    }
            else:
                return {
                    'status_code': 401,
                    'error': 'Invalid credentials!!!'
                }
        else:
            return {
                'status_code': 401,
                'message': 'You need to login'
            }

api.add_resource(RequestListApi, '/api/v1/requests', endpoint='requests')
api.add_resource(RequestApi, '/api/v1/requests/<string:r_id>', endpoint='request')


class ProposalListApi(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("user_proposed_to", type=str,
                                 help='Request host is required',
                                 required=True)

        self.parser.add_argument("user_proposed_from",
                                 type=str,
                                 help='Request guest is required',
                                 required=True)

        self.parser.add_argument("request",
                                 type=str,
                                 required=True)

        self.parser.add_argument("filled",
                                 type=bool,
                                 required=True)

        super(ProposalListApi, self).__init__()

    def get(self):
        token = request.args.get('token')
        if token:
            user = User.confirm_auth_token(token)
            if user:
                proposals = Proposal.objects()
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
                user_proposed_to = args['user_proposed_to']
                user_proposed_from = args['user_proposed_from']
                filled = args['filled']
                req = args['request']

                if user_proposed_to != user_proposed_from:
                    prop = Proposal.objects.get(request=req)
                    if not prop:
                        proposal = Proposal(user_proposed_from=user_proposed_from,
                                            user_proposed_to=user_proposed_to,
                                            filled=filled,
                                            request=req)
                        proposal.save()

                        return {
                            'status_code': 201,
                            'message': 'Proposal placed successfully'
                        }
                    else:
                        return {'status_code': 406, 'message': 'Request is already occupied'}
                else:
                    return {'status_code': 406, 'message': 'Cannot meet with yourself'}
            else:
                return {'status_code': 401, 'message': 'Invalid credentials!!!'}
        else:
            return {'status_code': 401, 'message': 'You need to login'}


class ProposalApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("user_proposed_to", type=str,
                                 help='Request host is required',
                                 required=True)

        self.parser.add_argument("user_proposed_from",
                                 type=str,
                                 help='Request guest is required',
                                 required=True)

        self.parser.add_argument("request",
                                 type=str,
                                 required=True)

        self.parser.add_argument("filled",
                                 type=bool,
                                 required=True)

        super(ProposalApi, self).__init__()

    def get(self, prop_id):
        token = request.args.get('token')
        if token:
            user = User.confirm_auth_token(token)
            if user:
                prop = Proposal.objects.get(id=prop_id)
                return {
                    'status_code': 200,
                    'requests': marshal(prop, proposal_fields)
                }
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
                p.user_proposed_to = ObjectId(args['user_proposed_to'])
                p.user_proposed_from = ObjectId(args['user_proposed_from'])
                p.filled = args['filled']
                p.req = ObjectId(args['request'])

                p.save()

                return {
                    'status_code': 200,
                    'message': 'Proposal updated'
                }
            else:
                return {'status_code': 401, 'message': 'Invalid credentials!!!'}
        else:
            return {'status_code': 401, 'message': 'You need to login'}

    def delete(self, prop_id):
        token = request.args.get('token')
        if token:
            user = User.confirm_auth_token(token)
            if user:
                Proposal.objects.get(id=prop_id).delete()

                return {
                    'status_code': 204,
                    'message': 'Proposal deleted successfully'
                }
            else:
                return {'status_code': 401, 'error': 'Invalid credentials!!!'}
        else:
            return {'status_code': 401, 'message': 'You need to login'}


api.add_resource(ProposalListApi, '/api/v1/proposals', endpoint='proposals')
api.add_resource(ProposalApi, '/api/v1/proposals/<string:prop_id>', endpoint='proposal')


class MealDateListApi(Resource):

    def get(self):
        pass

    def post(self):
        pass


class MealDateApi(Resource):

    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

api.add_resource(MealDateListApi, '/api/v1/mealdate', endpoint='mealdates')
api.add_resource(MealDateApi, '/api/v1/mealdate/<string:id>', endpoint='mealdate')






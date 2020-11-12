from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse
from src.model import model
from src.sqs_lib import send_message
from src.config import Config
##from loguru import logger

application = Flask(__name__)
api = Api(application)

getter = model.state_getter()

def auth_check(request):
    token = request.headers.get('Authorization')
    return token is None or token != Config.AUTH_TOKEN

class HealthCheck(Resource):

    def get(self):
        return {'status':'alive'}, 200

class get_data(Resource):
    def __init__(self):
        """
        This class serves to retrieve a request of a specific user at a specified datetime
        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('user_id',
                            type=int,
                            required=True,
                            help='We need a user_id to fetch data')
        parser.add_argument('time',
                            type=int,
                            required=True,
                            help='Time of requested state')

        self.parser = parser

    def get(self):
        """
        :return: state of user
        """
        if auth_check(request):
            return {'status':'unauthorized'}, 401

        args = self.parser.parse_args()
        result = getter.get_state(args.user_id, args.time)
        return result

class post_user(Resource):
    def __init__(self):
        """
        Create a new user
        """
    def post(self):
        """
        create a new user
        :return: the user
        """
        if auth_check(request):
            return {'status':'unauthorized'}, 401

        body = request.get_json()

        return getter.create_user(body['username'],body['password'],body['email'])

class post_data(Resource):
    def __init__(self):
        """
        This class serves to retrieve a request of a specific user at a specified datetime
        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('user_id',
                            type=int,
                            required=True,
                            help='We need to know the user_id of who this data belongs to')

        self.parser = parser

    def post(self):
        """
        receive raw data for a user
        :return: Status 200 if got data okay
        """
        if auth_check(request):
            return {'status':'unauthorized'}, 401

        args = self.parser.parse_args()
        body = request.get_json()

        getter.insert_gsr_values(args.user_id, body['timestamps'], body['gsr_values'])

        message_body = {'user_id': args.user_id, 'ts': body['timestamps'][0]} #needs to be the max ts
        send_message('scares', message_body)

        return 'Thank you for your data'

api.add_resource(HealthCheck, '/healthcheck')
api.add_resource(get_data, '/getdata')
api.add_resource(post_data, '/data')
api.add_resource(post_user, '/user')

if __name__ == '__main__':
    application.debug = True
    application.run()
from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse
from model.model import *
from sqs_lib import send_message


app = Flask(__name__)
api = Api(app)

model = state_getter()

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

        args = self.parser.parse_args()
        result = model.get_state(args.user_id, args.time)
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
        body = request.get_json()
        return model.create_user(body['username'],body['password'],body['email'])

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

        args = self.parser.parse_args()
        body = request.get_json()

        model.insert_gsr_values(args.user_id, body['timestamps'], body['gsr_values'])

        message_body = {'user_id': args.user_id, 'ts': body['timestamps'][0]} #needs to be the max ts
        send_message('scares', message_body)

        return 'Thank you for your data'

api.add_resource(HealthCheck, '/healthcheck')
api.add_resource(get_data, '/getdata')
api.add_resource(post_data, '/data')
api.add_resource(post_user, '/user')

if __name__ == '__main__':
    app.run(host='localhost', port='8080')

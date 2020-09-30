from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse
from datetime import datetime
from model.model import *


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

    
api.add_resource(HealthCheck, '/healthcheck')
api.add_resource(get_data, '/getdata')

if __name__ == '__main__':
    app.run(host='localhost', port='8080')
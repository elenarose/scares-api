from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse
from datetime import datetime
from model.model import *
import csv
import os


app = Flask(__name__)
api = Api(app)

model = state_getter()

class HealthCheck(Resource):

    def get(self):
        return {'status':'alive'}, 200

class get_latest_state(Resource):
    def __init__(self):
        """
        This class serves to retrieve a data request from a user of their latest state
        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('user_id',
                            type=int,
                            required=True,
                            help='We need a user_id to fetch data')

        self.parser = parser

    def get(self):
        """
        :return: state of user
        """

        args = self.parser.parse_args()
        result = model.get_state(args.user_id, args.time)
        return result

class update_user_data(Resource):
    def __init__(self):
        """
        this will be a post call
        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('user_id',
                            type=int,
                            required=True,
                            help='We need a user_id to fetch data')
        parser.add_argument('data',
                            type=csv, # could be just text, however their api sends it
                            required=True,
                            help='We need the data!')
        self.parser = parser

    def post(self):
        """

        :return:
        """
        os.system("touch 'resources/data.csv'")

        args = self.parser.parse_args()
        row = [args.user_id, args.data]
        with open('resources/data.csv', 'w') as f:
                csvwriter = csv.writer(f)
                csvwriter.writerow(row)



    
api.add_resource(HealthCheck, '/healthcheck')
api.add_resource(get_latest_state, '/getdata')

if __name__ == '__main__':
    app.run(host='localhost', port='8080')

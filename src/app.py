from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

#model = #name of model()

class HealthCheck(Resource):

    def get(self):
        return {'status':'alive'}, 200

class get_data(Resource):
    def __init__(self):
        """
        what is being returned here
        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('user_id',
                            type=int,
                            required=True,
                            help='We need a user_id to fetch data')

        self.parser = parser

    def get(self):
        """

        :return:
        """

        args = self.parser.parse_args()
        result = """model.return_requested_data"""
        return result

    
api.add_resource(HealthCheck, '/healthcheck')
api.add_resource(get_data, '/getdata')

if __name__ == '__main__':
    app.run(host='localhost', port='8080')
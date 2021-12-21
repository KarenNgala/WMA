from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self):
        data = pd.read_csv('users.csv') 
        data = data.to_dict()  
        return {'data': data}, 200 

class Payments(Resource):
    def patch(self):
        parser = reqparse.RequestParser()  # initialize parser
        parser.add_argument('paymentId', required=True, type=int)  # add args
        parser.add_argument('user_status', store_missing=False)  # name/rating are optional
        parser.add_argument('payment_status', store_missing=False)
        args = parser.parse_args()  # parse arguments to dictionary
        
        # read our CSV
        data = pd.read_csv('payments.csv')
        
        # check that the location exists
        if args['paymentId'] in list(data['paymentId']):
            # if it exists, we can update it, first we get user row
            user_data = data[data['paymentId'] == args['paymentId']]
            
            # if name has been provided, we update name
            if 'payment_status' in args:
                user_data['payment_status'] = args['payment_status']

            if args['payment_status'] == 'paid':
                user_data['user_status'] = 'is_premium'
            else:
                user_data['user_status'] = 'is_standard'
            
            # update data
            data[data['paymentId'] == args['paymentId']] = user_data
            # now save updated data
            data.to_csv('payments.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200
        
        else:
            # otherwise we return 404 not found
            return {
                'message': f"'{args['paymentId']}' payment record does not exist."
            }, 404

api.add_resource(Users, '/users')
api.add_resource(Payments, '/activate')

if __name__ == '__main__':
    app.run()
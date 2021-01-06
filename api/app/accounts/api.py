from flask_restful import Resource, Api
from app.accounts import accounts_bp

accounts_api = Api(accounts_bp)



class HelloWorld(Resource):
    def get(self):
        return {
            'backend': 'accounts app',
            }


accounts_api.add_resource(HelloWorld, '/')

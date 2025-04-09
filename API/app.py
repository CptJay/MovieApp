from flask import Flask, request
from flask_restful import Api, Resource
from flasgger import Swagger, swag_from
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')

### Initialize Flask app
app = Flask(__name__)
api = Api(app)

### Swagger configuration
app.config['SWAGGER'] = {
    'title': 'My API',
    'uiversion': 3,
    'openapi': '3.0.2',
}
swagger = Swagger(app)

class Test(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'A successful response',
                'examples': {
                    'application/json': {'message': 'Hello, World!zzz'}
                }
            }
        }
    })
    def get(self):
        """
        Test endpoint
        """
        return {'message': f'Hello, World! {API_KEY}'}, 200


# Link resources to URLs
api.add_resource(Test, '/')


if __name__ == '__main__':
    app.run(debug=True)

from flask_swagger_ui import get_swaggerui_blueprint
from flask import jsonify,json


SWAGGER_URL = '/swagger'
API_URL = 'swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "RESTful API for User model"
    }
)

@swaggerui_blueprint.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))
from flask import jsonify, request
from app import app
import app.database as database
from functools import wraps
import json

def logging_request(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        response_args = {
            'ip': request.remote_addr,
            'args': dict((key, request.args.get(key)) for key in request.args)
        }
        app.logger.info(response_args)
        return f(*args, **kwargs)

    return wrapper

@app.errorhandler(404)
def not_found(error=None):
    return jsonify({
        'code': 0,
        'response': 'Not Found'
    })


@app.route('/api/v1.0/add_user', methods=['GET'])
@logging_request
def add_user():
    user = request.args.get('user')
    user_json = json.loads(user)
    if 'email' not in user_json or \
            'username' not in user_json or \
            'full_name' not in user_json or \
            'information_bio' not in user_json or \
            'password' not in user_json:
        response = {'code': 409, 'response': 'Conflict'}
    elif database.Database().add_user(user):
        response = { 'code': 201, 'response': 'Created', 'type_api' : 'json'}
    else:
        response = {'code': 409,'response': 'Conflict', 'type_api' : 'json'}
    return jsonify(response)

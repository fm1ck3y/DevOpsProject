from flask import jsonify, request, render_template
from app import app
import app.database as database
from functools import wraps

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


@app.route('/api/v1.0/statistics', methods=['GET'])
@logging_request
def get_statistics():
    count_with_json = database.Database().count_users_json()
    count_without_json = database.Database().count_users_sql()

    return render_template('index.html', count_with_json=count_with_json, count_without_json= count_without_json)
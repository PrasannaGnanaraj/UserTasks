from flask import Flask, request, g , jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import random

DATABASE = {}
app = Flask(__name__)


@app.route('/signup', methods=['POST'])
def signup():
    return ({'success': True}, 200) if register_user(request.form.to_dict()) else ('record not found', 400)


@app.route('/login', methods=['POST'])
def login():
    print(request.get_json())
    username = request.get_json()['username']
    user = authenticate(username)
    if user:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return 'User not found', 400


@app.route('/requests')
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


def register_user(user_details):
    DATABASE[user_details['last_name']] = user_details
    DATABASE[user_details['last_name']]['id'] = random.randint(1, 101)
    return True


def authenticate(username):
    print(DATABASE.get(username, None))
    return DATABASE.get(username, None)


def identity(payload):
    user_id = payload['identity']
    return DATABASE.get(user_id, None)


if __name__ == '__main__':
    jwt = JWTManager(app)
    app.config.from_pyfile('config.cfg')
    app.run(host='0.0.0.0')








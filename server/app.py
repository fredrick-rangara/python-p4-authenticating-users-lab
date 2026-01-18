#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource

# Local imports
# We import app, db, and api from config to ensure they are the 
# same instances used by the models and tests.
from config import app, db, api
from models import User

# Resource Classes
class Login(Resource):
    def post(self):
        # 1. Get username from request JSON
        request_json = request.get_json()
        username = request_json.get('username')

        # 2. Retrieve user by username
        user = User.query.filter(User.username == username).first()

        if user:
            # 3. Set the session user_id
            session['user_id'] = user.id
            # 4. Return user and 200 status
            return user.to_dict(), 200
        
        return {'error': 'Invalid username'}, 401

class Logout(Resource):
    def delete(self):
        # 1. Remove the user_id from the session
        # Using .pop(key, default) is a safer way to clear session keys
        session.pop('user_id', None)
        
        # 2. Return no data and 204 status
        return {}, 204

class CheckSession(Resource):
    def get(self):
        # 1. Retrieve user_id from session
        user_id = session.get('user_id')
        
        # 2. If it exists, find the user and return them
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            if user:
                return user.to_dict(), 200
        
        # 3. If no user_id or user not found, return an EMPTY dict and 401
        # Change {'error': 'Unauthorized'} to {}
        return {}, 401

# Add Routes
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')

# Optional: Helper route for tests to clear the session
@app.route('/clear', methods=['GET'])
def clear_session():
    session.clear()
    return {}, 204

if __name__ == '__main__':
    app.run(port=5555, debug=True)
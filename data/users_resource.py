from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.users import User
from flask import Flask, render_template, redirect, jsonify, make_response


def abort_if_job_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"Job {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_job_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'users': user.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality',
                  'address', 'email', 'hashed_password'))})

    def delete(self, user_id):
        abort_if_job_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('hashed_password', required=True)


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'jobs': [item.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality',
                  'address', 'email', 'hashed_password')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            hashed_password=args['hashed_password']
        )
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})

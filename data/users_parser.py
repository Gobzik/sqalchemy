from flask_restful import reqparse


def make_users_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('surname', required=True)
    parser.add_argument('name', required=True)
    parser.add_argument('age', required=True, type=int)
    parser.add_argument('position', required=True)
    parser.add_argument('speciality', required=True)
    parser.add_argument('address', required=True)
    parser.add_argument('email', required=True)
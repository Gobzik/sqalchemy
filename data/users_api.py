import datetime
import flask
from flask import jsonify, make_response, request
from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'user':
                [item.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality',
                                    'address', 'email', 'modified_date', 'hashed_password'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'user': user.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality',
                                       'address', 'email', 'modified_date', 'hashed_password'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def add_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'position', 'speciality',
                  'address', 'email']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    user = User(
        id=request.json['id'],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        modified_date=datetime.datetime.now()
    )
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'id': user.id})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)

    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)

    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    required_fields = ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email']
    if not all(key in request.json for key in required_fields):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    user.surname = request.json['surname']
    user.name = request.json['name']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.email = request.json['email']
    user.modified_date = datetime.datetime.now()

    try:
        db_sess.commit()
        return jsonify({'success': 'OK'})
    except Exception as e:
        db_sess.rollback()
        return make_response(jsonify({'error': str(e)}), 500)

from flask import Flask, request, jsonify
from flask.views import MethodView
from db import User, Advert, Session
from schema import validate_user, validate_advert
from errors import HttpError
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

app = Flask('server')
bcrypt = Bcrypt(app)

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    http_response = jsonify({'status': 'error',
                             'description': error.message})
    http_response.status_code = error.status_code
    return http_response


def get_user(user_id: int, session: Session):
    user = session.query(User).get(user_id)
    if user is None:
        raise HttpError(404, 'user not found')
    return user


def get_user_by_name(username: str, session: Session):
    user = session.query(User).filter(User.username == username).first()
    if user is None:
        raise HttpError(404, 'user not found')
    return user


def get_advert(advert_id: int, session: Session):
    advert = session.query(Advert).get(advert_id)
    if advert is None:
        raise HttpError(404, 'advert not found')
    return advert


class UserView(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            return jsonify({'id': user_id,
                            'user_name': user.username,
                            'created_at': user.created_at.isoformat()})

    def post(self):
        json_data = validate_user(request.json)
        json_data['password'] = bcrypt.generate_password_hash(json_data['password']).decode()
        with Session() as session:
            new_user = User(**json_data)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'user already exists')
            return jsonify({
                'id': new_user.id,
                'created_at': new_user.created_at.isoformat(),
            })

    def patch(self, user_id: int):
        json_data = request.json
        with Session() as session:
            user = get_user(user_id, session)
            for field, value in json_data.items():
                setattr(user, field, value)
            session.add(user)
            session.commit()
        return jsonify({'status': 'success'})

    def delete(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            session.delete(user)
            session.commit()
            return jsonify({'status': 'success'})


class AdvertView(MethodView):

    def get(self, advert_id: int):
        with Session() as session:
            advert = get_advert(advert_id, session)
            return jsonify({'id': advert_id,
                            'caption': advert.caption,
                            'description': advert.description,
                            'created_at': advert.created_at,
                            'owner_id': advert.owner_id})

    def post(self):
        json_data = validate_advert(request.json, 'post')
        with Session() as session:
            user = get_user_by_name(json_data['user'], session)
            if not bcrypt.check_password_hash(user.password, json_data['password']):
                raise HttpError(401, 'incorrect password')
            new_advert = Advert(caption=json_data['caption'], description=json_data['description'],
                                owner_id=user.id)
            session.add(new_advert)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'can not add adverts. Not found owner by id')
            return jsonify({
                'id': new_advert.id,
                'caption': new_advert.caption,
                'created_at': new_advert.created_at.isoformat(),
            })

    def delete(self, advert_id: int):
        json_data = validate_advert(request.json, 'delete')
        with Session() as session:
            user = get_user_by_name(json_data['user'], session)
            if not bcrypt.check_password_hash(user.password, json_data['password']):
                raise HttpError(401, 'incorrect password')
            advert = get_advert(advert_id, session)
            session.delete(advert)
            session.commit()
            return jsonify({'status': 'success'})

    def patch(self, advert_id: int):
        json_data = validate_advert(request.json, 'patch')
        with Session() as session:
            user = get_user_by_name(json_data['user'], session)
            if not bcrypt.check_password_hash(user.password, json_data['password']):
                raise HttpError(401, 'incorrect password')
            advert = get_advert(advert_id, session)
            advert.caption = json_data['caption']
            advert.description = json_data['description']
            session.add(user)
            session.commit()
        return jsonify({'status': 'success'})


app.add_url_rule('/users/<int:user_id>', view_func=UserView.as_view('users_view'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/users', view_func=UserView.as_view('users_post'), methods=['POST'])
app.add_url_rule('/adverts/<int:advert_id>', view_func=AdvertView.as_view('adverts_view'), methods=['GET', 'DELETE',
                                                                                                    'PATCH'])
app.add_url_rule('/adverts', view_func=AdvertView.as_view('advert_post'), methods=['POST'])

app.run(port=5000)

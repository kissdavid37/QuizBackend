import uuid
import jwt
from app import Session
from flask import jsonify, make_response, request, Blueprint
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
import os
from Model.models import Users
import datetime
from flask_cors import cross_origin
from app import cors

auth_bp = Blueprint('auth', __name__)
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token=None
        s=Session()
        if 'x-access-token' in request.headers:
            token=request.headers['x-access-token']

        if not token:
            return jsonify({'message':'A valid token is missing'})
        try:
            data=jwt.decode(token,os.getenv('SECRET_KEY'),algorithms=['HS256'])
            current_user=s.query(Users).filter_by(publicId=data['publicId']).first()
            s.close()
        except:
            s.close()
            return jsonify({'message':'token is invalid'},401)
        return f(current_user, *args, **kwargs)
    return decorated

@auth_bp .route('/register',methods=['POST'])
def register():
    s=Session()
    data=request.get_json()
    username=data['username']
    password=data['password']
    confirm_password=data['confirm']
    if password != confirm_password:
        return make_response('Passwords do not match',400)
    if not username or not password:
        return make_response('Credentials cannot be empty!', 401)
    hashed_password=generate_password_hash(data['password'],method='sha256')
    new_user=Users(publicId=(uuid.uuid4()), username=data['username'],password=hashed_password,admin=0)
    s.add(new_user)
    s.commit()
    s.close()
    return data

@auth_bp .route('/login', methods=['POST'])
@cross_origin()
def login():
    s=Session()

    data=request.get_json()
    username=data['username']
    password=data['password']

    if not username or not password:
        s.close()
        return make_response('Could not verify', 401)

    user=s.query(Users).filter_by(username=username).first()
    s.close()

    if not user:
        return make_response('Username is incorrect', 401)

    if check_password_hash(user.password, password):
        token = jwt.encode({'publicId': user.publicId,'admin':user.admin, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)}, os.getenv('SECRET_KEY'))
        return jsonify({'token': token})

    return make_response('Bad password', 402)
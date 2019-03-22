# coding: utf-8

"""
    login.py
    ~~~~~~~~

    木犀官网登陆API

"""

from flask import jsonify, request
from . import auth
from ..models import User
from .. import db
import base64

@auth.route('/login/', methods=['POST'])
def login():
    username = request.get_json().get("username")
    pwd = request.get_json().get("password")
    try :
        pwd = base64.b64decode(pwd)
        pwd = unicode(pwd)
    except :
        return jsonify({ }) , 401
    if not username  :
        return jsonify({}) , 401
    user = User.query.filter_by(username=username).first()
    if not user:
        try:
            user = User.query.filter_by(email=username).first()
        except:
            return jsonify({}), 401
    if not user.verify_password(pwd):
        return jsonify({}), 400

    token = user.generate_auth_token()
    return jsonify ({
        'token': token,
        'user_id' : user.id ,
        }), 200


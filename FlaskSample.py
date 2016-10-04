# -*- coding: utf-8 -*-
import os
from flask import Flask, request, render_template, session
import json

app = Flask(__name__)


@app.route('/index')
def index():
    return '<a href="login">登录</a><br/><a href="userinfo">用户信息</a>'


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'GET':
        return render_template('decorator-login.html')
    else:
        user = {
            'user_name': request.form['user_name'],
            'password': request.form['password']
        }
        session['current_user'] = user
    return render_template('decorator-userinfo.html', user=user)


@app.route('/userinfo',methods=["GET","POST"])
def userinfo():
    user = session['current_user']
    if request.method == 'GET':
        return render_template('decorator-userinfo.html',user=user)
    else:
        if user is None:
            return json.dumps({'status':0})
        else:
            return json.dumps({'status':1,'user_name':user.user_name,'password':user.password})


@app.route('/getpath/<string:path_type>',methods=['GET','POST'])
def getroot(path_type):
    if path_type is None or len(path_type) == 0:
        return 'path type is none'
    elif path_type == 'static':
        return os.path.dirname(os.path.abspath(__file__))
    return 'unable path type'


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=9000)


import requests
import random
import string

from flask import Flask,request,render_template,jsonify
from flask_cors import CORS
from pymongo import MongoClient
from flask_pymongo import PyMongo
from flask_login import LoginManager
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'linx000'
app.config['MONGO_URI'] ='mongodb://localhost:27017/Pet_Hospital'
mongo = PyMongo(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

#随机用户名
def rand_username(length = 10):
    characters = string.ascii_letters + string.digits
    random_chars = random.choices(characters, k=length)
    return ''.join(random_chars)

#随机密码
def rand_password(length = 10):
    characters = string.ascii_letters + string.digits
    random_chars = random.choices(characters, k=length)
    return ''.join(random_chars)


#登录
@app.route('/wx_login',methods=['POST'])
def login():
    code = request.json.get('code')
    if not code:
        return jsonify({'errmsg':"缺少登录凭证code",'errcode':-1}),400  
    appid = 'wxba313964554e47bf'
    secret = 'ff099c444733206fb29a98de62861bf7'
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'
    response = requests.get(url)
    data = response.json()
    openid = data.get('openid')
    session_key = data.get('session_key')

    if not openid or not session_key:
        return jsonify({'errmsg':"登录失败",'errcode':-1}),400
    
    username = rand_username()
    User = mongo.db.user.find_one({'openid':openid})
    if User['openid'] == openid:
        print('该用户已注册')
    else: 
        print('该用户未注册')
        mongo.db.user.insert_one({'openid':openid,'username':username})
        User = {'openid': openid, 'username': username, 'pets': None}
    user = {
    "openid": User['openid'],
    "img": User['img'],
    "username": User['username'],
    "pets": User.get('pets')
    }
    return jsonify(user),200



if __name__ == '__main__':
    app.run(host='192.168.31.55',port=5000,debug=True)
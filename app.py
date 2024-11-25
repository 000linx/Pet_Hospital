from Class import User
from flask_cors import CORS
from flask_pymongo import PyMongo
from utils import rand_username,get_data, user_to_dict
from flask import Flask,request,jsonify 


app = Flask(__name__)
app.config['SECRET_KEY'] = 'linx000'
app.config['MONGO_URI'] ='mongodb://localhost:27017/Pet_Hospital'
mongo = PyMongo(app)
CORS(app)

@app.route('/wx_login',methods = ['POST'])
def login():
    code = request.json.get('code')
    data = get_data(code)
    openid = data.get('openid')
    session_key = data.get('session_key')

    if not openid or not session_key:
        return jsonify({'errmsg':"登录失败",'errcode':-1}),400
    user = mongo.db.user.find_one({'openid':openid})
    if user:
        print('登录成功')
        login_user = User(user['openid'],user['username'],user['phone'],user['img'],user['pets'])
        return user_to_dict(login_user),200
    else:
        print('该用户未注册')
        username = rand_username()
        new_user = User(openid,username,'','',[])
        mongo.db.user.insert_one({'openid':openid,'username':username,'phone':'','img':'','pets':[]})
        return jsonify(user_to_dict(new_user)),200
    

if __name__ == '__main__':
    app.run(host='192.168.31.56',port=5000,debug=True)
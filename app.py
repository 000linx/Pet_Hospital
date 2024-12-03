
from flask import Flask,request,jsonify 
from pymongo import MongoClient
from flask_cors import CORS
from config import *
from utils import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'linx000'
# 数据库设置
client = MongoClient('localhost', 27017)
db = client['Pet_Hospital']
user_collection = db['user']
doctor_collection = db['doctor']
appointment_collection = db['appointment']
CORS(app)

'''
接口名

/wx_login 登录
/wx_updateuser 更新用户信息
/wx_addpet 添加宠物
/wx_getpet 获取宠物信息
/wx_updatepet 更新宠物信息
/wx_deletepet 删除宠物
/wx_doctor 获取医生信息
/wx_doctors 获取全部医生信息
/wx_appointment 预约挂号 
/wx_cancel_appointment 取消预约 
/wx_get_appointment 获取单个预约信息
/wx_get_appointments 获取全部预约信息
'''


'''
用户方法
登录
修改信息

'''

#登录
@app.route('/wx_login',methods = ['POST'])
def login():
    code = request.json.get('code')
    data = get_data(code)
    openid = data.get('openid')
    session_key = data.get('session_key')
    if not openid or not session_key:
        return jsonify({'errmsg':"登录失败",'errcode':-1}),400
    user = find_user(openid)
    if not user:
        print('没有该用户,已经自动创建')
        username = generate_rand_username()
        user = User(openid,username,'','/pages/img/用户头像.png',pets = {})
        user = user.__dict__()
        user_collection.insert_one(user)
    else :
        print('登录成功')
    return jsonify({'errmsg':'ok','errcode':0,'user_data':user}),200

# 更新用户信息
@app.route('/wx_updateuser', methods=['POST'])
def updateuser():
    data = request.json
    openid = data.get('openid')
    user = find_user(openid)
    if not user:
        print('没有该用户')
        return jsonify({'errmsg':"没有该用户",'errcode':-1}),400
    else:
        user['username'] = data['username']
        user['phone'] = data['phone']
        user['img'] = data['img']
        user_collection.update_one({'openid':openid},{'$set':{'username':user['username'],'phone':user['phone'],'img':user['img']}})
    return jsonify({'errmsg':"更新成功",'errcode':0,'user_data':user}),200

# 注销账户
@app.route('/wx_canceluser',methods = ['POST'])
def canceluser():
    data = request.json
    openid = data.get('openid')
    print(openid)
    user = find_user(openid)
    if not user:
        print('没有该用户')
        return jsonify({'errmsg':"没有该用户",'errcode':-1}),400
    else:
        user_collection.delete_one({'openid':openid})
        appointment_collection.delete_many({'openid':openid})
    return jsonify({'errmsg':"注销成功",'errcode':0}),200

'''
宠物方法
添加宠物
获取宠物信息
更新宠物信息
删除宠物

'''

#添加宠物
@app.route('/wx_addpet',methods = ['POST'])
def add_pet():
    data = request.json
    openid = data.get('openid')
    pets = data.get('pets')
    new_pet = Pets(pets['petType'],pets['petName'],pets['petAvatar'],pets['variety'],pets['date'],pets['gender'],pets['neutered']).__dict__()
    user = find_user(openid)
    if user['pets'] is not None:
        if new_pet['petName'] in [pet['petName'] for pet in user['pets']]:
            print('已经有该宠物')
            return jsonify({'errmsg':"已经有该宠物",'errcode':-1}),400
        else:
            user['pets'].append(new_pet)
    else :
        print('已添加该宠物')
        user['pets'].append(new_pet)
    user_collection.update_one({'openid':openid},{'$set':{'pets':user['pets']}})
    return jsonify({'errmsg':"添加成功",'errcode':0,'pet_data':user['pets']}),200

# 获取单个宠物信息
@app.route('/wx_getpet', methods=['POST'])
def getpet():
    data = request.json
    openid = data.get('openid')
    petName = data.get('petName')
    user = find_user(openid)
    if user['pets'] is not None:
        for i in range(len(user['pets'])):
            if user['pets'][i]['petName'] == petName:
                return jsonify({'errmsg':"ok",'errcode':0,'pet_data':user['pets'][i]}),200
        else:
            print('没有该宠物')
            return jsonify({'errmsg':"没有该宠物",'errcode':-1}),400
    else:
        print('没有该宠物')
        return jsonify({'errmsg':"没有该宠物",'errcode':-1}),400


# 更新宠物信息
@app.route('/wx_updatepet', methods=['POST'])
def updatepet():
    data = request.json
    openid = data.get('openid')
    pet = data.get('pet')
    oldpetName = data.get('oldPetName')
    user = find_user(openid)
    if user['pets'] is not None:
        for i in range(len(user['pets'])):
            if user['pets'][i]['petName'] == oldpetName:
                user['pets'][i]['petName'] = pet['petName']
                user['pets'][i]['petAvatar'] = pet['petAvatar']
                user['pets'][i]['variety'] = pet['variety']
                user['pets'][i]['date'] = pet['date']
                user['pets'][i]['gender'] = pet['gender']
                user['pets'][i]['neutered'] = pet['neutered']
                user_collection.update_one({'openid':openid},{'$set':{'pets':user['pets']}})
                break
        else:
            print('没有该宠物')
            return jsonify({'errmsg':"没有该宠物",'errcode':-1}),400
    return jsonify({'errmsg':"更新成功",'errcode':0,'pet_data':user['pets']}),200

# 删除宠物
@app.route('/wx_deletepet', methods=['POST'])
def deletepet():
    data = request.json
    openid = data.get('openid')
    petName = data.get('PetName')
    user = find_user(openid)
    if user['pets'] is not None:
        for i in range(len(user['pets'])):
            if user['pets'][i]['petName'] == petName:
                user['pets'].pop(i)
                break
        else:
            print('没有该宠物')
            return jsonify({'errmsg':"没有该宠物",'errcode':-1}),400
        user_collection.update_one({'openid':openid},{'$set':{'pets':user['pets']}})
    return jsonify({'errmsg':"删除成功",'errcode':0,'pet_data':user['pets']}),200

'''
医生方法
获取医生信息
获取全部医生信息
'''

#获取单个医生信息
@app.route('/wx_doctor',methods = ['POST'])
def get_doctor():
    data = request.json
    docid = data.get('docid')
    doctor = find_doctor(docid)
    if not doctor:
        print('没有该医生')
        return jsonify({'errmsg':"没有该医生",'errcode':-1}),400
    else:
        return jsonify({'errmsg':"ok",'errcode':0,'doctor_data':doctor}),200

# 获取全部医生信息
@app.route('/wx_doctors',methods = ['GET'])
def get_all_doctor():
    doctors = find_all_doctor()
    return jsonify({'errmsg':"ok",'errcode':0,'doctor_data':list(doctors)}),200


'''
预约方法
预约挂号
取消预约
获取用户预约信息
'''
# 预约挂号
@app.route('/wx_appointment',methods = ['POST'])
def appointment():
    data = request.json
    orderid = generate_order_number()
    new_appointment = Appointment(data['openid'],data['pet'],data['date'],data['doc'],data['userName'],data['phone'],orderid).__dict__()
    print(new_appointment)
    appointment_collection.insert_one(new_appointment)
    return jsonify({'errmsg':"预约成功",'errcode':0}),200

# 取消预约
@app.route('/wx_cancel_appointment',methods = ['POST'])
def cancel_appointment():
    data = request.json
    orderid = data.get('orderid')
    appointment_collection.delete_one({'orderid':orderid})
    return jsonify({'errmsg':"取消成功",'errcode':0}),200

# 获取单个预约信息
@app.route('/wx_get_appointment',methods = ['POST'])
def get_appointment():
    data = request.json
    orderid = data.get('orderid')
    appointment = appointment_collection.find_one({'orderid':orderid},{'_id':0})
    if not appointment:
        print('没有该预约')
        return jsonify({'errmsg':"没有该预约",'errcode':-1}),400
    else:
        return jsonify({'errmsg':"ok",'errcode':0,'appointment_data':appointment}),200
    
# 获取用户全部预约信息
@app.route('/wx_get_appointments',methods = ['POST'])
def get_appointments():
    data = request.json
    openid = data.get('openid')
    appointments = appointment_collection.find({'openid':openid},{'_id':0})
    if not appointments:
        print('暂无预约信息')
        return jsonify({'errmsg':"暂无预约信息",'errcode':-1}),400
    else:
        return jsonify({'errmsg':"ok",'errcode':0,'appointment_data':list(appointments)}),200


if __name__ == '__main__':
    app.run(host='192.168.121.16',port=5000,debug=True)
import random
import string
from pymongo import MongoClient
import requests
from flask import jsonify
from config import User,Doctor
# 连接到MongoDB
client = MongoClient('localhost', 27017)
# 选择数据库和集合
db = client['Pet_Hospital']
user_collection = db['user']
doctor_collection = db['doctor']

# 获取数据
def get_data(code):
    if not code:
        return jsonify({'errmsg':"缺少登录凭证code",'errcode':-1}),400
    appid = 'wxba313964554e47bf'
    secret = 'ff099c444733206fb29a98de62861bf7'
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'
    response = requests.get(url)
    data = response.json()
    return data

# 用户名生成
def generate_rand_username():
    characters = string.ascii_letters + string.digits
    random_chars = random.choices(characters, k=10)
    return 'CY_'+''.join(random_chars)
# 订单号生成
def generate_order_number():
    order_number = 'CYD' + ''.join(random.choices(string.digits, k=16))
    return order_number
    # 根据openid查找用户
def find_user(openid):
    user = user_collection.find_one({'openid':openid})
    if user:
        user = User(user['openid'],user['username'],user['phone'],user['img'],user['pets'])
        return user.__dict__()
    else:
        return None
# 查找单个医生
def find_doctor(docid):
    doctor = doctor_collection.find_one({'docid':docid})
    if doctor:
        doctor = Doctor(doctor['docid'],doctor['name'],doctor['pet'],doctor['position'],doctor['img'],doctor['specialties'],doctor['DoctorProfile'])
        return doctor.__dict__()
    else:
        return None
# 获取全部医生
def find_all_doctor():
    doctors = doctor_collection.find({},{'_id':0})
    if doctors:
        return doctors
    else:
        return None



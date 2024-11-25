import random
import string
import requests
from flask import jsonify

# 随机用户名
def rand_username(length = 10):
    characters = string.ascii_letters + string.digits
    random_chars = random.choices(characters, k=length)
    return ''.join(random_chars)

#获取数据
def get_data(code):
    if not code:
        return jsonify({'errmsg':"缺少登录凭证code",'errcode':-1}),400
    appid = 'wxba313964554e47bf'
    secret = 'ff099c444733206fb29a98de62861bf7'
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'
    response = requests.get(url)
    data = response.json()
    return data

# 将Pet对象转换为字典
def pets_to_dict(pets):
    return {
        'Pet_type': pets.Pet_type,
        'name': pets.name,
        'img': pets.img,
        'pet_breed': pets.pet_breed,
        'birthday': pets.birthday,
        'sex': pets.sex,
        'is_sterilized': pets.is_sterilized
    }

# 将User对象转换为字典
def user_to_dict(user):
    return {
        'openid': user.openid,
        'username': user.username,
        'phone': user.phone,
        'img': user.img,
        'pets': [pets_to_dict(pet) for pet in user.pets]
    }
    
class User():
    def __init__(self,openid,username,phone,img,pets):
        self.openid = openid
        self.username = username
        self.phone = phone
        self.img = img
        self.pets = pets

class Doctor():
    def __init__(self,openid,name,phone,img,patients):
        self.openid = openid
        self.name = name
        self.phone = phone
        self.img = img
        self.patients = patients

class Pets():
    def __init__(self,Pet_type,name,img,pet_breed,birthday,sex,is_sterilized):
        self.Pet_type = Pet_type
        self.name = name
        self.img = img
        self.pet_breed = pet_breed
        self.birthday = birthday
        self.sex = sex
        self.is_sterilized = is_sterilized



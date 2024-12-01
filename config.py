class User():
    def __init__(self,openid,username,phone,img,pets = {}):
        self.openid = openid
        self.username = username
        self.phone = phone
        self.img = img
        self.pets = pets
    # 添加用户
    def add_user(self,collection):
        collection.insert_one(self.__dict__())

    # 添加宠物
    def add_pet(self,pet):
        self.pets.append(pet)
    
    # 转化为字典
    def __dict__(self):
        return {
            'openid': self.openid,
            'username': self.username,
            'phone': self.phone,
            'img': self.img,
            'pets': self.pets
        }
class Doctor():
    def __init__(self,docid,name,pet,position,img,specialties,DoctorProfile):
        self.docid = docid
        self.name = name
        self.pet = pet
        self.position = position
        self.img = img
        self.specialties = specialties
        self.DoctorProfile = DoctorProfile
    def __dict__(self):
        return {
            'docid': self.docid,
            'name': self.name,
            'pet': self.pet,
            'position': self.position,
            'img': self.img,
            'specialties': self.specialties,
            'DoctorProfile': self.DoctorProfile
        }

class Pets():
    def __init__(self,petType,petName,petAvatar,variety,date,gender,neutered):
        self.petType = petType
        self.petName = petName
        self.petAvatar = petAvatar
        self.variety = variety
        self.date = date
        self.gender = gender
        self.neutered = neutered
    
    def __dict__(self):
        return {
            'petType': self.petType,
            'petName': self.petName,
            'petAvatar': self.petAvatar,
            'variety': self.variety,
            'date': self.date,
            'gender': self.gender,
            'neutered': self.neutered
        }

class Appointment():
    def __init__(self,openid,pet,date,doc,userName,phone,orderid):
        self.openid = openid
        self.pet = pet
        self.date = date
        self.doc = doc
        self.userName = userName
        self.phone = phone
        self.orderid = orderid
    def __dict__(self):
        return {
            'openid': self.openid,
            'pet': self.pet,
            'date': self.date,
            'doc': self.doc,
            'userName': self.userName,
            'phone': self.phone,
            'orderid': self.orderid
        }

class Test:
    def __init__(self,id,name,pets = []):
        self.id = id
        self.name = name
        self.pets = pets

    def __dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'pets': self.pets
        }
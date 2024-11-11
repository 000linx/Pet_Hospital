from flask import Flask,request,render_template
from flask_cors import CORS
from pymongo import MongoClient
from flask_pymongo import PyMongo
from flask_login import LoginManager
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['MONGO_URI'] ='mongodb://localhost:27017/mydatabase'
mongo = PyMongo(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.route('/login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = mongo.db.users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            return 'Login successful'
        else:
            return 'Invalid username or password'
    return render_template('login.html')
@app.route('register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        mongo.db.users.insert_one({'username': username, 'password': hashed_password})
        return 'Registration successful'
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
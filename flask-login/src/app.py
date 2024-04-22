import sqlite3
from flask import Flask, render_template, redirect, url_for, request, flash
from flask import g
from flask_wtf import CSRFProtect
from ModelUser import User, ModelUser
from config import config 
from flask_login import LoginManager, login_user, logout_user, login_required

app = Flask(__name__)

DATABASE = 'login-db.db'
TABLE = 'LOG_DB'

csrf = CSRFProtect()

login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(DATABASE, id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #print(request.form['username'])
        #print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(DATABASE, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("invalid pass")
                return render_template('auth/login.html')
        else:
            flash("User Not found")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/protected')
@login_required
def protected():
    return "<h1>esta es una vista protegida</h1>"

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>pagina no encontrada</h1>"


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
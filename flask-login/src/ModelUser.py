import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password, entreprise='') -> None:
        self.id = id
        self.username = username
        self.password = password
        self.entreprise = entreprise

    @classmethod
    def check_password(self, hashed_pass, password):
        return check_password_hash(hashed_pass, password)

class ModelUser():
    @classmethod
    def login(self, db, user):
        try:
            conn = sqlite3.connect(db)
            cursor = conn.cursor()
            query = ("""SELECT id, username, password, entreprise FROM LOG_DB
                           WHERE username ='{}'""".format(user.username))
            cursor.execute(query)
            row = cursor.fetchone()
            conn.close()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), '12')
                return user
            else:
                return None
        
        except Exception as e:
            return Exception(e)
        
    @classmethod
    def get_by_id(self, db, id):
        try:
            conn = sqlite3.connect(db)
            cursor = conn.cursor()
            query = ("""SELECT id, username, entreprise FROM LOG_DB
                           WHERE id ='{}'""".format(id))
            cursor.execute(query)
            row = cursor.fetchone()
            conn.close()
            if row != None:
                logged_user = User(row[0], row[1], None, row[2])
                return logged_user
            else:
                return None
        
        except Exception as e:
            return Exception(e)
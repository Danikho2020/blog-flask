from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    emails = db.Column(db.String(40))
    password = db.Column(db.String(255))
    comments = db.relationship('Comment') #esto es para la relacion con la otra tabla
    created_date = db.Column(db.DateTime, default= datetime.datetime.now) #esto guardará la fecha y la hora del momento de creacion

    @classmethod
    def create(cls, username):
            user = User(username=username)
            return user.save()

    def __init__(self, username, emails, password):
        self.username = username
        self.emails = emails
        self.password = self.__create_pasword(password) #al constructor le decimos que la contraseña la obtendra del metodo que sigue


    #este método devuelve la contraseña encriptada
    def __create_pasword(self, password):
        return generate_password_hash(password)
    #este método 'desencripta' la contraseña para verificarla durante el login
    def verify_password(self, password):
        return check_password_hash(self.password, password)


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,  db.ForeignKey('users.id') )# así le damos la foreign key
    text = db.Column(db.Text())
    created_date = db.Column(db.DateTime, default= datetime.datetime.now)
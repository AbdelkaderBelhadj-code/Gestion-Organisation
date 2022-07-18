# http://webdamn.com/user-management-system-with-python-flask-and-mysql/*

import enum
from flask_login import UserMixin

from datetime import timedelta
from flask import Flask
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
import  pymysql
import os

from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "secret key"
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)
CORS(app)
host='localhost'
user='root'
passwd=''
database='organisation'
#variables for my database in order to connect
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+user+':'+passwd+'@'+host+'/'+database
#Connect to mysql database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app) 

# class UserRoleEnum(enum.Enum):
#     superAdmin = 'SuperAdmin'
#     adminOrg = 'AdminOrg'
#     user = 'user'

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    date_adhesion = db.Column(db.DateTime(),nullable=False)
    tel = db.Column(db.Integer,nullable=False)

    avatar_photo = db.Column(db.String(100), nullable=False, server_default=u' ')
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users',
                                               lazy='dynamic'))
    def __init__(self, nom, prenom, password, email, date_adhesion, tel, avatar_photo, roles):

        self.nom = nom
        self.prenom = prenom
        self.password = password
        self.email = email
        self.date_adhesion = date_adhesion
        self.tel = tel
        self.avatar_photo = avatar_photo
        self.roles = roles

        
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
# UserRoles - Table
class UserRoles(db.Model):
    __tablename__ = 'users_roles'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)




# Espacclass Event(db.Model):
class EspaceOrganisation(db.Model):
    __tablename__ = 'espaces'
    id = db.Column(db.Integer(), primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    presentation = db.Column(db.String(2000), nullable=False)
    objectifs = db.Column(db.String(2000), nullable=False)
    reglement_int = db.Column(db.String(20000), nullable=False, server_default=u' ')

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer(), primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(200), nullable=False)
  
class Evenement(db.Model):
    __tablename__ = 'evenements'
    id = db.Column(db.Integer(), primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    date_debut = db.Column(db.DateTime(),nullable=False)
    date_fin = db.Column(db.DateTime(),nullable=False)
    heure = db.Column(db.Integer)
    lieu = db.Column(db.String(200), nullable=False)
    document = db.Column(db.String(200), nullable=False)
    rappels = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = db.relationship('User', backref=db.backref('user'))

    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    documents = db.relationship('Document', backref=db.backref('user'))


class UserEvenemet(db.Model):
    __tablename__ = 'users_evenements'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    evenement_id = db.Column(db.Integer(), db.ForeignKey('evenements.id', ondelete='CASCADE'), primary_key=True)

class Tache(db.Model):
    __tablename__ = 'taches'
    id = db.Column(db.Integer(), primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    date_debut = db.Column(db.DateTime(),nullable=False)
    date_fin = db.Column(db.DateTime(),nullable=False)
    lieu = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(2000), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = db.relationship('User', backref=db.backref('user'))

class UserTache(db.Model):
    __tablename__ = 'users_taches'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    tache_id = db.Column(db.Integer(), db.ForeignKey('taches.id', ondelete='CASCADE'), primary_key=True)

class Sondage(db.Model):
    __tablename__ = 'sondages'
    id = db.Column(db.Integer(), primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    date_debut = db.Column(db.DateTime(),nullable=False)
    date_fin = db.Column(db.DateTime(),nullable=False)
    lieu = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    nbr_rappels = db.Column(db.Integer)
    options = db.Column(db.Boolean, default=False, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = db.relationship('User', backref=db.backref('user'))

class UserSondage(db.Model):
    __tablename__ = 'users_sondages'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    sondage_id = db.Column(db.Integer(), db.ForeignKey('sondages.id', ondelete='CASCADE'), primary_key=True)

class Proposition(db.Model):
    __tablename__ = 'proposition'
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(2000), nullable=False)

class Historique(db.Model):
    __tablename__ = 'historique'
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(2000), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = db.relationship('User', backref=db.backref('user'))
db.create_all()
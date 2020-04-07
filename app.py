# flash  错误提示
from flask import Flask, render_template, url_for,redirect,request,flash
from flask_sqlalchemy import SQLAlchemy
import sys, os

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'  # windows平台
else:
    prefix = 'sqlite:////'  # Mac   Linux平台

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Flask
app.config['SECRET_KEY'] = '123'
db = SQLAlchemy(app)
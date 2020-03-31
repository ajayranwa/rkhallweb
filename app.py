from flask import Flask, render_template, redirect, url_for, request, session, logging, flash
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email
from functools import wraps
from flask_ckeditor import CKEditorField
# import mysql.connector
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=False)
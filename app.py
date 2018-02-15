# --- Modules/Functions --- #

import os , sys , cgi , re, hmac, hashlib, smtplib, requests, datetime
import logging, dateutil, sqlite3, urllib, httplib2, json, psycopg2
import random, string, bcrypt

from functools import wraps
from datetime import timedelta
from threading import Timer
from dateutil import parser

from flask import Flask, make_response, g, request, send_from_directory
from flask import render_template, url_for, redirect, flash, jsonify
from flask import session as user_session
from werkzeug.utils import secure_filename
from jinja2.ext import do

import chamber
from chamber import uniqueValue

import routes_get
import routes_post
import routes_put
import routes_delete



# --- Setup --- #

app = Flask(__name__)
app.secret_key = 'DF6Y#6G1$56*4G!?/Eoifht496dfgs3TYD5$)F&*DFj/Y4R'

def login_required(f):
    ''' Checks If User Is Logged In '''
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'session_id' in user_session:
            return f(*args, **kwargs)
        else:
            flash('Please Log In To Use This Site.')
            return redirect('/login')

    return decorated_function
# ---

def logged_in():
    return 'session_id' in user_session and 'user_id' in user_session
# ---

def Authorize(f):
    ''' Checks If Client Is Authorized '''
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'auth_key' in user_session:
            return f(*args, **kwargs)
        else:
            return jsonify(error = True, message = 'client is NOT authorized')

    return decorated_function
# ---

def Check_Authorize():
    return 'auth_key' in user_session
# ---


# --- GET Routes --- #



@app.route('/', methods=['GET'])
def welcome():
    return routes_get.welcome(request)


@app.route('/signup', methods=['GET'])
def signup_get():
    return routes_get.signup(request)


@app.route('/signin', methods=['GET'])
def signin_get():
    return routes_get.signin(request)


@app.route('/signout', methods=['GET'])
def signout_get():
    return routes_get.signout(request)



@app.route('/faq', methods=['GET'])
def faq():
    return routes_get.faq(request)


@app.route('/about', methods=['GET'])
def about():
    return routes_get.about(request)


@app.route('/info', methods=['GET'])
def info():
    return routes_get.info(request)



@app.route('/check_session', methods=['GET'])
def check_session():
    return routes_get.check_session(request)


@app.route('/profile', methods=['GET'])
def profile():
    return routes_get.profile(request)



# --- POST Routes --- #




@app.route('/signup', methods=['POST'])
def signup_post():
    return routes_post.signup(request)





# --- PUT Routes --- #




@app.route('/signin', methods=['PUT'])
def signin_put():
    return routes_put.signin(request)




# --- DELETE Routes --- #







# --- API Routes --- #







# --- Listen --- #

# print(db_session)
if __name__ == '__main__':
    app.debug = True
    app.run( host = '0.0.0.0' , port = 5000 )

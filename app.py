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



# --- GET Routes --- #



@app.route('/', methods=['GET'])
def welcome():
    return routes_get.welcome(request)



# --- POST Routes --- #







# --- PUT Routes --- #








# --- DELETE Routes --- #







# --- API Routes --- #







# --- Listen --- #

# print(db_session)
if __name__ == '__main__':
    app.debug = True
    app.run( host = '0.0.0.0' , port = 5000 )

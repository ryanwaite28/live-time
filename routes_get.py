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

from sqlalchemy import cast, exc, select
from sqlalchemy import desc, or_
from sqlalchemy.sql import func
from sqlalchemy.exc import InvalidRequestError, ArgumentError
from sqlalchemy.exc import StatementError, OperationalError, InternalError
from jinja2.ext import do

import models
from models import Base, db_session

from models import Accounts, Featured, Follows
from models import Events, EventPerformers, EventRequests
from models import Notifications
from models import ChatRooms, ChatRoomMembers, ChatRoomMessages

import chamber
from chamber import uniqueValue




def logged_in():
    return 'session_id' in user_session and 'account_id' in user_session
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




def welcome(request):
    user_session['auth_key'] = uniqueValue()
    return render_template('welcome.html', session = logged_in())


def faq(request):
    user_session['auth_key'] = uniqueValue()
    return render_template('faq.html', session = logged_in())


def about(request):
    user_session['auth_key'] = uniqueValue()
    return render_template('about.html', session = logged_in())


def info(request):
    user_session['auth_key'] = uniqueValue()
    return render_template('info.html', session = logged_in())


def signup(request):
    user_session['auth_key'] = uniqueValue()
    if 'session_id' in user_session:
        return redirect('/')

    return render_template('signup.html', session = logged_in())


def signin(request):
    user_session['auth_key'] = uniqueValue()
    if 'session_id' in user_session:
        return redirect('/')

    return render_template('signin.html', session = logged_in())


def signout(request):
    if 'session_id' in user_session:
        you = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()

        you.last_loggedout = func.now()
        db_session.add(you)
        db_session.commit()

    user_session.clear()
    return redirect('/')


@Authorize
def check_session(request):
    if 'session_id' in user_session:
        you = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()
        return jsonify(online = True, account = you.serialize)

    else:
        return jsonify(online = False)



def check_auth(request):
    if 'auth_key' in user_session:
        return jsonify(auth = True, message = 'client is authorized')

    else:
        return jsonify(auth = False, message = 'client is NOT authorized')


def profile(request):
    if 'session_id' not in user_session:
        return redirect('/')

    user_session['auth_key'] = uniqueValue()
    return render_template('profile.html', session = logged_in())


def account_settings(request):
    if 'session_id' not in user_session:
        return redirect('/')

    user_session['auth_key'] = uniqueValue()
    return render_template('account-settings.html', session = logged_in())

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




@Authorize
def signup(request):
    try:
        data = json.loads(request.data)
        if not data:
            return jsonify( error = True, message = 'request body is empty, check headers/data' )

        print(data)

        username                   = str(data['username']).encode()
        account_email              = str(data['account_email']).encode()
        booking_email              = str(data['booking_email']).encode()
        account_type               = str(data['account_type']).encode()

        password                   = str(data['password']).encode()
        hashed                     = bcrypt.hashpw(password, bcrypt.gensalt())

        check_username             = db_session.query(Accounts).filter_by(username = username).first()
        check_account_email        = db_session.query(Accounts).filter_by(email = account_email).first()
        check_booking_email        = db_session.query(Accounts).filter_by(booking_email = booking_email).first()

        if check_username:
            return jsonify(error = True, message = 'username is already in use')

        if check_account_email:
            return jsonify(error = True, message = 'account email is already in use')

        if check_booking_email:
            return jsonify(error = True, message = 'booking email is already in use')

        new_account = Accounts(username = username, email = account_email, booking_email = booking_email, password = hashed, type = account_type)
        db_session.add(new_account)
        db_session.commit()

        session_id                     = chamber.uniqueValue()
        user_session['session_id']     = session_id
        user_session['account_id']     = new_account.id

        return jsonify(account = new_account.serialize, message = 'Signed Up!')

    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error signing up...')

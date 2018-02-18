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
def signin(request):
    try:
        data = json.loads(request.data)
        if not data:
            return jsonify( error = True, message = 'request body is empty, check headers/data' )

        print(data)

        email      = str(data['email']).encode()
        password   = str(data['password']).encode()

        account    = db_session.query(Accounts).filter_by(email = email).first()

        if not account:
            return jsonify(error = True, message = 'invalid credentials')

        if bcrypt.checkpw(password, account.password.encode()) == False:
            return jsonify(error = True, message = 'invalid credentials')

        session_id                     = chamber.uniqueValue()
        user_session['session_id']     = session_id
        user_session['account_id']     = account.id

        return jsonify(account = account.serialize, message = 'Signed In!')

    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error signing in...')



@Authorize
def update_info(request):
    try:
        data = json.loads(request.data)
        if not data:
            return jsonify(error = True, message = 'request body is empty, check headers/data')

        bio                = str(data['bio']).encode()
        categories         = str(data['categories']).encode()
        location           = str(data['location']).encode()
        link               = str(data['link']).encode()
        displayname        = str(data['displayname']).encode()
        phone              = str(data['phone']).encode()
        account_type       = str(data['type']).encode()

        you                = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()

        you.bio            = bio
        you.categories     = categories
        you.location       = location
        you.link           = link
        you.displayname    = displayname
        you.phone          = phone
        you.type           = account_type

        db_session.add(you)
        db_session.commit()

        return jsonify(account = you.serialize, message = 'Info Updated Successfully!')

    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')



@Authorize
def update_icon(request):
    try:
        if 'icon_photo' not in request.files:
            return jsonify(error = True, message = 'file with filename "icon_photo" was not found in request')

        file = request.files['icon_photo']
        if file and file.filename != '' and chamber.allowed_photo(file.filename):
            prev_ref               = request.form['prev_ref']

            link                   = chamber.uploadFile(file = file, prev_ref = prev_ref)

            you                    = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()
            you.icon               = link

            db_session.add(you)
            db_session.commit()

            return jsonify(account = you.serialize, message = 'Icon Updated Successfully!', icon = link)

        else:
            return jsonify(error = True, message = 'file with filename "icon_photo" was not of type: image')


    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')



@Authorize
def update_background(request):
    try:
        if 'background_photo' not in request.files:
            return jsonify(error = True, message = 'file with filename "background_photo" was not found in request')

        file = request.files['background_photo']
        if file and file.filename != '' and chamber.allowed_photo(file.filename):
            prev_ref               = request.form['prev_ref']

            link                   = chamber.uploadFile(file = file, prev_ref = prev_ref)

            you                    = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()
            you.background         = link

            db_session.add(you)
            db_session.commit()

            return jsonify(account = you.serialize, message = 'Background Updated Successfully!', background = link)

        else:
            return jsonify(error = True, message = 'file with filename "background_photo" was not of type: image')


    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')



@Authorize
def update_social(request):
    try:
        data = json.loads(request.data)
        if not data:
            return jsonify(error = True, message = 'request body is empty, check headers/data')

        facebook          = str(data['facebook']).encode()
        twitter           = str(data['twitter']).encode()
        youtube           = str(data['youtube']).encode()
        instagram         = str(data['instagram']).encode()
        soundcloud        = str(data['soundcloud']).encode()
        snapchat          = str(data['snapchat']).encode()
        itunes            = str(data['itunes']).encode()
        google_play       = str(data['google_play']).encode()
        last_fm           = str(data['last_fm']).encode()
        spotify           = str(data['spotify']).encode()
        google_plus       = str(data['google_plus']).encode()
        tidal             = str(data['tidal']).encode()
        pandora           = str(data['pandora']).encode()
        last_fm           = str(data['last_fm']).encode()
        spinrilla         = str(data['spinrilla']).encode()
        bandcamp          = str(data['bandcamp']).encode()

        you                    = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()

        you.facebook           = facebook
        you.twitter            = twitter
        you.youtube            = youtube
        you.instagram          = instagram
        you.soundcloud         = soundcloud
        you.snapchat           = snapchat
        you.itunes             = itunes
        you.google_play        = google_play
        you.last_fm            = last_fm
        you.spotify            = spotify
        you.google_plus        = google_plus
        you.tidal              = tidal
        you.pandora            = pandora
        you.last_fm            = last_fm
        you.spinrilla          = spinrilla
        you.bandcamp           = bandcamp

        db_session.add(you)
        db_session.commit()

        return jsonify(account = you.serialize, message = 'Social Updated Successfully!')

    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')



@Authorize
def update_username(request):
    try:
        data = json.loads(request.data)
        if not data:
            return jsonify(error = True, message = 'request body is empty, check headers/data')

        username          = str(data['username']).encode()

        check_username    = db_session.query(Accounts).filter_by(username = username).first()
        if check_username:
            return jsonify(error = True, message = 'username is already in use')


        you               = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()
        you.username      = username

        db_session.add(you)
        db_session.commit()

        return jsonify(account = you.serialize, message = 'Username Updated Successfully!')

    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')



@Authorize
def update_account_email(request):
    try:
        data = json.loads(request.data)
        if not data:
            return jsonify(error = True, message = 'request body is empty, check headers/data')

        email          = str(data['email']).encode()

        check_email    = db_session.query(Accounts).filter_by(email = email).first()
        if check_email:
            return jsonify(error = True, message = 'account email is already in use')


        you            = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()
        you.email      = email

        db_session.add(you)
        db_session.commit()

        return jsonify(account = you.serialize, message = 'Account Email Updated Successfully!')

    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')



@Authorize
def update_booking_email(request):
    try:
        data = json.loads(request.data)
        if not data:
            return jsonify(error = True, message = 'request body is empty, check headers/data')

        booking_email          = str(data['booking_email']).encode()

        check_email            = db_session.query(Accounts).filter_by(booking_email = booking_email).first()
        if check_email:
            return jsonify(error = True, message = 'booking account email is already in use')


        you                    = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()
        you.booking_email      = booking_email

        db_session.add(you)
        db_session.commit()

        return jsonify(account = you.serialize, message = 'Booking Email Updated Successfully!')

    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')


@Authorize
def update_password(request):
    try:
        data = json.loads(request.data)
        if not data:
            return jsonify(error = True, message = 'request body is empty, check headers/data')

        password               = str(data['password']).encode()
        hashed                 = bcrypt.hashpw(password, bcrypt.gensalt())


        you                    = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()
        you.password           = hashed

        db_session.add(you)
        db_session.commit()

        return jsonify(account = you.serialize, message = 'Password Updated Successfully!')

    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')

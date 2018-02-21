# --- Modules/Functions --- #

import os , sys , cgi , re, hmac, hashlib, smtplib, requests, datetime
import HTMLParser
import logging, dateutil, sqlite3, urllib, httplib2, json, psycopg2
import random, string, bcrypt

from functools import wraps
from datetime import datetime, timedelta
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
from models import EventLikes, EventComments, CommentLikes
from models import EventInvites, EventAttendees
from models import ArtistReviews, EventReviews
from models import Notifications
from models import ChatRooms, ChatRoomMembers, ChatRoomMessages
from models import Conversations, ConversationMessages

import chamber
from chamber import uniqueValue




def logged_in():
    return 'session_id' in user_session and 'account_id' in user_session
# ---





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




def create_event(request):
    try:
        if logged_in() == False:
            return jsonify(error = True, message = 'no session found with this request.')

        if not request.form:
            return jsonify(error = True, message = 'no request form was sent')

        print(request.form)

        you = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()
        if you.type != "VENUE":
            return jsonify(error = True, message = 'current user is not a VENUE')

        title             = str(request.form['title']).encode()
        desc              = str(request.form['desc']).encode()
        categories        = str(request.form['categories']).encode()
        location          = str(request.form['location']).encode()
        link              = str(request.form['link']).encode()
        date_concat       = str(request.form['date_concat']).encode()
        event_date_time   = datetime.strptime(date_concat, '%Y-%m-%d %H:%M:%S')

        if 'event_photo' not in request.files:
            icon = ''
        else:
            file = request.files['event_photo']
            if file and file.filename != '' and chamber.allowed_photo(file.filename):
                icon = chamber.uploadFile(file = file, prev_ref = '')
            else:
                icon = ''

        new_event = Events(title = title, desc = desc, categories = categories, location = location,
                            link = link, icon = icon, event_date_time = event_date_time, host_id = you.id)
        db_session.add(new_event)
        db_session.commit()

        return jsonify(message = 'Event Created Successfully!', event = new_event.serialize)


    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')



def toggle_event_like(request, event_id):
    check = db_session.query(EventLikes) \
    .filter_by(event_id = event_id) \
    .filter_by(owner_id = user_session['account_id']) \
    .first()

    if check:
        db_session.delete(check)
        db_session.commit()

        return jsonify(message = 'unliked', liked = False)

    else:
        like = EventLikes(event_id = event_id, owner_id = user_session['account_id'])
        db_session.add(like)
        db_session.commit()

        return jsonify(message = 'liked', liked = True)


def toggle_comment_like(request, comment_id):
    check = db_session.query(CommentLikes) \
    .filter_by(comment_id = comment_id) \
    .filter_by(owner_id = user_session['account_id']) \
    .first()

    if check:
        db_session.delete(check)
        db_session.commit()

        return jsonify(message = 'unliked', liked = False)

    else:
        like = CommentLikes(comment_id = comment_id, owner_id = user_session['account_id'])
        db_session.add(like)
        db_session.commit()

        return jsonify(message = 'liked', liked = True)



def create_event_comment(request, event_id):
    event = db_session.query(Events).filter_by(id = event_id).first()
    if not event:
        return jsonify(error = True, message = 'event not found')


    data = json.loads(request.data)
    if not data:
        return jsonify( error = True, message = 'request body is empty, check headers/data' )
    if 'text' not in data:
        return jsonify( error = True, message = 'no text key/value pair in request body' )


    text = str(data['text']).encode()

    new_comment = EventComments(event_id = event_id, owner_id = user_session['account_id'], text = text)
    db_session.add(new_comment)
    db_session.commit()

    return jsonify(message = 'event comment created', comment = new_comment.serialize)

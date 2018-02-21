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


def profile_events(request):
    user_session['auth_key'] = uniqueValue()

    if 'session_id' not in user_session:
        return render_template('error-page.html', session = logged_in(), message = 'Not logged in...')

    you = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()
    if you.type != 'VENUE':
        message = '''Your account is not of type: VENUE.
        Only Venues can have events.'''
        return render_template('error-page.html', session = logged_in(), message = message)

    return render_template('profile-events.html', session = logged_in())


def profile_shows(request):
    user_session['auth_key'] = uniqueValue()

    if 'session_id' not in user_session:
        return render_template('error-page.html', session = logged_in(), message = 'Not logged in...')

    you = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()
    if you.type != 'ARTIST':
        message = '''Your account is not of type: ARTIST.
        Only Artists can have shows.'''
        return render_template('error-page.html', session = logged_in(), message = message)

    return render_template('profile-shows.html', session = logged_in())


def profile_attending(request):
    user_session['auth_key'] = uniqueValue()

    if 'session_id' not in user_session:
        return render_template('error-page.html', session = logged_in(), message = 'Not logged in...')

    you = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()
    if you.type != 'USER':
        message = '''Your account is not of type: USER.
        Only Users can attend events.'''
        return render_template('error-page.html', session = logged_in(), message = message)

    return render_template('profile-attending.html', session = logged_in())



def account_page(request, username):
    user_session['auth_key'] = uniqueValue()

    account = db_session.query(Accounts).filter_by(username = username).first()

    if account == None:
        message = '''No account exists with this username'''
        return render_template('error-page.html', session = logged_in(), message = message)

    return render_template('user-page.html', session = logged_in())


def account_events(request, username):
    user_session['auth_key'] = uniqueValue()

    account = db_session.query(Accounts).filter_by(username = username).first()

    if account == None:
        message = '''No account exists with this username'''
        return render_template('error-page.html', session = logged_in(), message = message)

    if account.type != 'VENUE':
        message = '''This account is not of type: VENUE. Only Venues can have events.'''
        return render_template('error-page.html', session = logged_in(), message = message)

    return render_template('user-events.html', session = logged_in())


def account_shows(request, username):
    user_session['auth_key'] = uniqueValue()

    account = db_session.query(Accounts).filter_by(username = username).first()

    if account == None:
        message = '''No account exists with this username'''
        return render_template('error-page.html', session = logged_in(), message = message)

    if account.type != 'ARTIST':
        message = '''This account is not of type: ARTIST. Only Artists can have shows.'''
        return render_template('error-page.html', session = logged_in(), message = message)

    return render_template('user-shows.html', session = logged_in())


def account_attending(request, username):
    user_session['auth_key'] = uniqueValue()

    account = db_session.query(Accounts).filter_by(username = username).first()

    if account == None:
        message = '''No account exists with this username'''
        return render_template('error-page.html', session = logged_in(), message = message)

    if account.type != 'USER':
        message = '''This account is not of type: USER. Only Users can attend events.'''
        return render_template('error-page.html', session = logged_in(), message = message)

    return render_template('user-attending.html', session = logged_in())


def event_page(request, event_id):
    user_session['auth_key'] = uniqueValue()

    event = db_session.query(Events).filter_by(id = event_id).first()

    if event == None:
        message = '''No event exists with this id'''
        return render_template('error-page.html', session = logged_in(), message = message)

    return render_template('event-page.html', session = logged_in())



def create_event(request):
    user_session['auth_key'] = uniqueValue()

    if 'session_id' not in user_session:
        return render_template('error-page.html', session = logged_in(), message = 'Not logged in...')

    you = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()
    if you.type != 'VENUE':
        message = '''Your account is not of type: VENUE.
        Only Venues can create events.'''
        return render_template('error-page.html', session = logged_in(), message = message)

    return render_template('create-event.html', session = logged_in())


def edit_event(request, event_id):
    user_session['auth_key'] = uniqueValue()

    if 'session_id' not in user_session:
        return render_template('error-page.html', session = logged_in(), message = 'Not logged in...')

    event = db_session.query(Events).filter_by(id = event_id).first()

    if event == None:
        message = '''Event not found.'''
        return render_template('error-page.html', session = logged_in(), message = message)

    if event.host_id != user_session['account_id']:
        message = '''You cannot make edits because
        you do not own this event'''
        return render_template('error-page.html', session = logged_in(), message = message)

    return render_template('edit-event.html', session = logged_in())


def signin(request):
    user_session['auth_key'] = uniqueValue()
    return render_template('signin.html', session = logged_in())


def signout(request):
    if 'session_id' in user_session:
        you = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()

        you.last_loggedout = func.now()
        db_session.add(you)
        db_session.commit()

    user_session.clear()
    return redirect('/')



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





def get_event(request, event_id):
    event = db_session.query(Events).filter_by(id = event_id).first()
    if event:
        return jsonify(message = 'venue event', event = event.serialize)
    else:
        return jsonify(message = 'no venue event found', event = False)


def get_account_by_username(request, username):
    account = db_session.query(Accounts).filter_by(username = username).first()
    if account:
        return jsonify(message = 'account found', account = account.serialize)
    else:
        return jsonify(message = 'no account found', account = False)


def get_venue_events(request, account_id, event_id):
    if event_id == 0:
        events = db_session.query(Events) \
        .filter(Events.host_id == account_id) \
        .order_by(desc(Events.date_created)) \
        .limit(5) \
        .all()

    else:
        events = db_session.query(Events) \
        .filter(Events.host_id == account_id) \
        .filter(Events.id < event_id) \
        .order_by(desc(Events.date_created)) \
        .limit(5) \
        .all()

    return jsonify(message = 'venue events', events = [e.serialize for e in events])


def get_artist_shows(request, account_id, event_performer_id):
    if event_performer_id == 0:
        shows = db_session.query(EventPerformers) \
        .filter(EventPerformers.performer_id == account_id) \
        .order_by(desc(EventPerformers.date_created)) \
        .limit(5) \
        .all()

    else:
        shows = db_session.query(EventPerformers) \
        .filter(EventPerformers.performer_id == account_id) \
        .filter(EventPerformers.id < event_performer_id) \
        .order_by(desc(EventPerformers.date_created)) \
        .limit(5) \
        .all()

    return jsonify(message = 'artist shows', shows = [s.serialize for s in shows])


def get_user_attending(request, account_id, attend_id):
    if attend_id == 0:
        attending = db_session.query(EventAttendees) \
        .filter(EventAttendees.account_id == account_id) \
        .order_by(desc(EventAttendees.date_created)) \
        .limit(5) \
        .all()

    else:
        attending = db_session.query(EventAttendees) \
        .filter(EventAttendees.account_id == account_id) \
        .filter(EventAttendees.id < attend_id) \
        .order_by(desc(EventAttendees.date_created)) \
        .limit(5) \
        .all()

    return jsonify(message = 'user attending', attending = [a.serialize for a in attending])



def check_event_account_like(request, event_id, account_id):
    check = db_session.query(EventLikes) \
    .filter_by(event_id = event_id) \
    .filter_by(owner_id = account_id) \
    .first()

    if check:
        return jsonify(message = 'liked', liked = True)
    else:
        return jsonify(message = 'not liked', liked = False)


def check_comment_account_like(request, comment_id, account_id):
    check = db_session.query(CommentLikes) \
    .filter_by(comment_id = comment_id) \
    .filter_by(owner_id = account_id) \
    .first()

    if check:
        return jsonify(message = 'liked', liked = True)
    else:
        return jsonify(message = 'not liked', liked = False)


def check_account_follow(request, account_id):
    if account_id == user_session['account_id']:
        return jsonify(error = True, message = 'provided account_id is same as session account\'s id')

    check = db_session.query(Follows) \
    .filter_by(account_id = user_session['account_id']) \
    .filter_by(follows_id = account_id) \
    .first()

    if check:
        return jsonify(message = 'following', following = True)
    else:
        return jsonify(message = 'not following', following = False)


def get_event_comments(request, event_id, comment_id):
    try:
        if comment_id == 0:
            event_comments = db_session.query(EventComments) \
            .filter(EventComments.event_id == event_id) \
            .order_by(desc(EventComments.date_created)) \
            .limit(5) \
            .all()

        else:
            event_comments = db_session.query(EventComments) \
            .filter(EventComments.event_id == event_id) \
            .filter(EventComments.id < comment_id) \
            .order_by(desc(EventComments.date_created)) \
            .limit(5) \
            .all()

        return jsonify(message = 'event comments', event_comments = [ec.serialize for ec in event_comments])


    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')



def search_events(request, search_type, search_query):
    try:
        search_type = str(search_type).encode().lower().replace('_space_', ' ').replace('%20', ' ')
        types = ['location', 'category']
        if search_type not in types:
            return jsonify(error = True, message = 'search type is unknown/invalid: ' + search_type)


        query = '%' + str(cgi.escape(search_query)).encode().lower() + '%'

        if search_type == 'location':
            events = db_session.query(Events) \
            .filter( func.lower(Events.location).like( query ) ) \
            .order_by(func.random()) \
            .limit(10).all()

        if search_type == 'category':
            events = db_session.query(Events) \
            .filter( func.lower(Events.categories).like( query ) ) \
            .order_by(func.random()) \
            .limit(10).all()


        return jsonify(message = 'events', events = [e.serialize for e in events])


    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')



def search_venues(request, search_type, search_query):
    try:
        search_type = str(search_type).encode().lower().replace('_space_', ' ').replace('%20', ' ')
        types = ['location', 'category', 'username']
        if search_type not in types:
            return jsonify(error = True, message = 'search type is unknown/invalid: ' + search_type)


        query = '%' + str(cgi.escape(search_query)).encode().lower() + '%'

        if search_type == 'username':
            venues = db_session.query(Accounts) \
            .filter(Accounts.type == 'VENUE') \
            .filter( func.lower(Accounts.username).like( query ) ) \
            .order_by(func.random()) \
            .limit(10).all()

        if search_type == 'location':
            venues = db_session.query(Accounts) \
            .filter(Accounts.type == 'VENUE') \
            .filter( func.lower(Accounts.location).like( query ) ) \
            .order_by(func.random()) \
            .limit(10).all()

        if search_type == 'category':
            venues = db_session.query(Accounts) \
            .filter(Accounts.type == 'VENUE') \
            .filter( func.lower(Accounts.categories).like( query ) ) \
            .order_by(func.random()) \
            .limit(10).all()


        return jsonify(message = 'venues', venues = [v.serialize for v in venues])


    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')



def search_artists(request, search_type, search_query):
    try:
        search_type = str(search_type).encode().lower().replace('_space_', ' ').replace('%20', ' ')
        types = ['location', 'category', 'username']
        if search_type not in types:
            return jsonify(error = True, message = 'search type is unknown/invalid: ' + search_type)


        query = '%' + str(cgi.escape(search_query)).encode().lower() + '%'

        if search_type == 'username':
            artists = db_session.query(Accounts) \
            .filter(Accounts.type == 'ARTIST') \
            .filter( func.lower(Accounts.username).like( query ) ) \
            .order_by(func.random()) \
            .limit(10).all()

        if search_type == 'location':
            artists = db_session.query(Accounts) \
            .filter(Accounts.type == 'ARTIST') \
            .filter( func.lower(Accounts.location).like( query ) ) \
            .order_by(func.random()) \
            .limit(10).all()

        if search_type == 'category':
            artists = db_session.query(Accounts) \
            .filter(Accounts.type == 'ARTIST') \
            .filter( func.lower(Accounts.categories).like( query ) ) \
            .order_by(func.random()) \
            .limit(10).all()


        return jsonify(message = 'artists', artists = [a.serialize for a in artists])


    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')



def search_users(request, search_type, search_query):
    try:
        search_type = str(search_type).encode().lower().replace('_space_', ' ').replace('%20', ' ')
        types = ['location', 'category', 'username']
        if search_type not in types:
            return jsonify(error = True, message = 'search type is unknown/invalid: ' + search_type)


        query = '%' + str(cgi.escape(search_query)).encode().lower() + '%'

        if search_type == 'username':
            users = db_session.query(Accounts) \
            .filter(Accounts.type == 'USER') \
            .filter( func.lower(Accounts.username).like( query ) ) \
            .order_by(func.random()) \
            .limit(10).all()

        if search_type == 'location':
            users = db_session.query(Accounts) \
            .filter(Accounts.type == 'USER') \
            .filter( func.lower(Accounts.location).like( query ) ) \
            .order_by(func.random()) \
            .limit(10).all()

        if search_type == 'category':
            users = db_session.query(Accounts) \
            .filter(Accounts.type == 'USER') \
            .filter( func.lower(Accounts.categories).like( query ) ) \
            .order_by(func.random()) \
            .limit(10).all()


        return jsonify(message = 'artists', users = [u.serialize for u in users])


    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')

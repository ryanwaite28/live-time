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


def SessionRequired(f):
    ''' Checks If Client Is Authorized '''
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'session_id' in user_session and 'account_id' in user_session:
            return f(*args, **kwargs)
        else:
            return jsonify(error = True, message = 'no session found with this request.')

    return decorated_function
# ---


def Check_Authorize():
    return 'auth_key' in user_session
# ---



def create_notification(id, msg, link):
    new_notification = Notifications(account_id = id, message = msg, link = link)
    db_session.add(new_notification)
    db_session.commit()
    return new_notification



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


@app.route('/search', methods=['GET'])
def search_page():
    return routes_get.search_page(request)


@Authorize
@app.route('/check_session', methods=['GET'])
def check_session():
    return routes_get.check_session(request)


@app.route('/profile', methods=['GET'])
def profile():
    return routes_get.profile(request)


@app.route('/account_settings', methods=['GET'])
def account_settings():
    return routes_get.account_settings(request)


@app.route('/profile/events', methods=['GET'])
def profile_events():
    return routes_get.profile_events(request)


@app.route('/profile/shows', methods=['GET'])
def profile_shows():
    return routes_get.profile_shows(request)


@app.route('/profile/attending', methods=['GET'])
def profile_attending():
    return routes_get.profile_attending(request)


@app.route('/accounts/<username>', methods=['GET'])
def account_page(username):
    return routes_get.account_page(request, username)


@app.route('/venue/<username>/events', methods=['GET'])
def account_events(username):
    return routes_get.account_events(request, username)


@app.route('/artist/<username>/shows', methods=['GET'])
def account_shows(username):
    return routes_get.account_shows(request, username)


@app.route('/user/<username>/attending', methods=['GET'])
def account_attending(username):
    return routes_get.account_attending(request, username)


@app.route('/event/<int:event_id>', methods=['GET'])
def event_page(event_id):
    return routes_get.event_page(request, event_id)


@app.route('/create/event', methods=['GET'])
def create_event_get():
    return routes_get.create_event(request)


@app.route('/event/<int:event_id>/edit', methods=['GET'])
def edit_event(event_id):
    return routes_get.edit_event(request, event_id)


@Authorize
@app.route('/get/account/<username>', methods=['GET'])
def get_account_by_username(username):
    return routes_get.get_account_by_username(request, username)


@Authorize
@app.route('/get/event/<int:event_id>', methods=['GET'])
def get_event(event_id):
    return routes_get.get_event(request, event_id)


@Authorize
@app.route('/venue/<int:account_id>/events/<int:event_id>', methods=['GET'])
def get_venue_events(account_id, event_id):
    return routes_get.get_venue_events(request, account_id, event_id)


@Authorize
@app.route('/artist/<int:account_id>/shows/<int:event_performer_id>', methods=['GET'])
def get_artist_shows(account_id, event_performer_id):
    return routes_get.get_artist_shows(request, account_id, event_performer_id)


@Authorize
@app.route('/user/<int:account_id>/attending/<int:attend_id>', methods=['GET'])
def get_user_attending(account_id, attend_id):
    return routes_get.get_user_attending(request, account_id, attend_id)


@Authorize
@SessionRequired
@app.route('/event/<int:event_id>/account_like/<int:account_id>', methods=['GET'])
def check_event_account_like(event_id, account_id):
    return routes_get.check_event_account_like(request, event_id, account_id)


@Authorize
@SessionRequired
@app.route('/comment/<int:comment_id>/account_like/<int:account_id>', methods=['GET'])
def check_comment_account_like(comment_id, account_id):
    return routes_get.check_comment_account_like(request, comment_id, account_id)


@Authorize
@SessionRequired
@app.route('/accounts/<int:account_id>/following', methods=['GET'])
def check_account_follow(account_id):
    return routes_get.check_account_follow(request, account_id)


# the comment_id is used as a starting point for the query:
# filter comments by IDs greater than the comment id given
@Authorize
@app.route('/event/<int:event_id>/comments/<int:comment_id>', methods=['GET'])
def get_event_comments(event_id, comment_id):
    return routes_get.get_event_comments(request, event_id, comment_id)


@Authorize
@app.route('/search/events/<search_type>/<search_query>', methods=['GET'])
def search_events(search_type, search_query):
    return routes_get.search_events(request, search_type, search_query)


@Authorize
@app.route('/search/venues/<search_type>/<search_query>', methods=['GET'])
def search_venues(search_type, search_query):
    return routes_get.search_venues(request, search_type, search_query)


@Authorize
@app.route('/search/artists/<search_type>/<search_query>', methods=['GET'])
def search_artists(search_type, search_query):
    return routes_get.search_artists(request, search_type, search_query)


@Authorize
@app.route('/search/users/<search_type>/<search_query>', methods=['GET'])
def search_users(search_type, search_query):
    return routes_get.search_users(request, search_type, search_query)




@Authorize
@app.route('/get/random/events', methods=['GET'])
def get_random_events():
    return routes_get.get_random_events(request)


@Authorize
@app.route('/get/random/venues', methods=['GET'])
def get_random_venues():
    return routes_get.get_random_venues(request)


@Authorize
@app.route('/get/random/artists', methods=['GET'])
def get_random_artists():
    return routes_get.get_random_artists(request)


@Authorize
@app.route('/get/random/users', methods=['GET'])
def get_random_users():
    return routes_get.get_random_users(request)



# --- POST Routes --- #



@Authorize
@app.route('/signup', methods=['POST'])
def signup_post():
    return routes_post.signup(request)


@Authorize
@SessionRequired
@app.route('/venue/create_event', methods=['POST'])
def create_event_post():
    return routes_post.create_event(request)


@Authorize
@SessionRequired
@app.route('/event/<int:event_id>/create_comment', methods=['POST'])
def create_event_comment(event_id):
    return routes_post.create_event_comment(request, event_id)


@Authorize
@SessionRequired
@app.route('/event/<int:event_id>/toggle_like', methods=['POST'])
def toggle_event_like(event_id):
    return routes_post.toggle_event_like(request, event_id)


@Authorize
@SessionRequired
@app.route('/comment/<int:comment_id>/toggle_like', methods=['POST'])
def toggle_comment_like(comment_id):
    return routes_post.toggle_comment_like(request, comment_id)


@Authorize
@SessionRequired
@app.route('/accounts/<int:account_id>/toggle_follow', methods=['POST'])
def toggle_account_follow(account_id):
    return routes_post.toggle_account_follow(request, account_id)




# --- PUT Routes --- #



@Authorize
@app.route('/signin', methods=['PUT'])
def signin_put():
    return routes_put.signin(request)



@Authorize
@SessionRequired
@app.route('/account/update_info', methods=['PUT'])
def update_info():
    return routes_put.update_info(request)


@Authorize
@SessionRequired
@app.route('/account/update_icon', methods=['PUT'])
def update_icon():
    return routes_put.update_icon(request)


@Authorize
@SessionRequired
@app.route('/account/update_background', methods=['PUT'])
def update_background():
    return routes_put.update_background(request)


@Authorize
@SessionRequired
@app.route('/account/update_social', methods=['PUT'])
def update_social():
    return routes_put.update_social(request)


@Authorize
@SessionRequired
@app.route('/account/update_username', methods=['PUT'])
def update_username():
    return routes_put.update_username(request)


@Authorize
@SessionRequired
@app.route('/account/update_account_email', methods=['PUT'])
def update_account_email():
    return routes_put.update_account_email(request)


@Authorize
@SessionRequired
@app.route('/account/update_booking_email', methods=['PUT'])
def update_booking_email():
    return routes_put.update_booking_email(request)


@Authorize
@SessionRequired
@app.route('/account/update_password', methods=['PUT'])
def update_password():
    return routes_put.update_password(request)


@Authorize
@SessionRequired
@app.route('/event/<int:event_id>/update', methods=['PUT'])
def update_event(event_id):
    return routes_put.update_event(request, event_id)


@Authorize
@SessionRequired
@app.route('/comment/<int:comment_id>/edit', methods=['PUT'])
def edit_comment(comment_id):
    return routes_put.edit_comment(request, comment_id)




# --- DELETE Routes --- #



@Authorize
@SessionRequired
@app.route('/account/delete', methods=['DELETE'])
def delete_account():
    return routes_delete.delete_account(request)


@Authorize
@SessionRequired
@app.route('/event/<int:event_id>/delete', methods=['DELETE'])
def delete_event(event_id):
    return routes_delete.delete_event(request, event_id)


@Authorize
@SessionRequired
@app.route('/comment/<int:comment_id>/delete', methods=['DELETE'])
def delete_comment(comment_id):
    return routes_delete.delete_comment(request, comment_id)



# --- API Routes --- #







# --- Listen --- #

# print(db_session)
if __name__ == '__main__':
    app.debug = True
    app.run( host = '0.0.0.0' , port = 5000 )

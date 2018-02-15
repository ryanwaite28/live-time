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

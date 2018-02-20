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





def delete_account(request):
    try:
        you = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()
        db_session.delete(you)
        db_session.comit()

        user_session.clear()
        return jsonify(error = False, message = 'Account Deleted')

    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')


def delete_event(request, event_id):
    try:
        event = db_session.query(Accounts).filter_by(id = event_id).first()
        if event == None:
            return jsonify(error = True, message = 'Event not found')

        db_session.delete(you)
        db_session.comit()

        return jsonify(error = False, message = 'Event Deleted')

    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')

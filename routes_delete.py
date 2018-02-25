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
from models import Conversations, ConversationMessages, Messages

import chamber
from chamber import uniqueValue
from chamber import ARTIST_EVENT_STATUSES, ACTION_TYPES, TARGET_TYPES, ERROR_TYPES




def logged_in():
    return 'session_id' in user_session and 'account_id' in user_session
# ---





def delete_account(request, sse):
    try:
        if 'account_id' not in user_session:
            return jsonify(error = True, message = 'no current session id...')

        you = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()
        db_session.delete(you)
        db_session.commit()

        user_session.clear()
        return jsonify(error = False, message = 'Account Deleted')

    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')


def delete_event(request, sse, event_id):
    try:
        event = db_session.query(Events) \
        .filter(Events.id == event_id) \
        .filter(Events.host_id == user_session['account_id']) \
        .first()
        if event == None:
            return jsonify(error = True, message = 'Event not found')

        db_session.delete(event)

        check_notifications = db_session.query(Notifications) \
        .filter(Notifications.target_type == TARGET_TYPES['EVENT']) \
        .filter(Notifications.target_id == event.id) \
        .all()

        if len(check_notifications) > 0:
            db_session.delete(check_notifications)

        db_session.commit()

        return jsonify(error = False, message = 'Event Deleted')

    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')



def delete_comment(request, sse, comment_id):
    try:
        comment = db_session.query(EventComments) \
        .filter(EventComments.id == comment_id) \
        .filter(EventComments.owner_id == user_session['account_id']) \
        .first()

        if not comment:
            return jsonify(error = True, message = 'No Comment Found...')

        db_session.delete(comment)

        check_notifications = db_session.query(Notifications) \
        .filter(Notifications.target_type == TARGET_TYPES['COMMENT']) \
        .filter(Notifications.target_id == comment.id) \
        .all()

        if len(check_notifications) > 0:
            db_session.delete(check_notifications)

        db_session.commit()

        return jsonify(message = 'Comment Deleted!')

    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')

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



def cancel_booking(request, sse, booking_id, account_id):
    try:
        # check given data

        your_id = user_session['account_id']
        if your_id == account_id:
            return jsonify(error = True, message = 'provided account_id is same as session\'s account_id')

        booking = db_session.query(EventPerformers) \
        .filter(EventPerformers.id == booking_id) \
        .filter( (EventPerformers.performer_id == your_id) | (EventPerformers.performer_id == account_id) ) \
        .first()

        if not booking:
            return jsonify(error = True, booking = False, message = 'no booking exists')

        # delete booking request and old notification

        check_notification = db_session.query(Notifications) \
        .filter(Notifications.action == ACTION_TYPES['BOOKED']) \
        .filter(Notifications.target_type == TARGET_TYPES['EVENT']) \
        .filter(Notifications.target_id == booking.event_rel.id) \
        .filter(Notifications.from_id == your_id) \
        .filter(Notifications.account_id == account_id) \
        .first()

        if check_notification:
            db_session.delete(check_notification)


        # create notification / push event

        you = db_session.query(Accounts).filter_by(id = your_id).one()
        account = db_session.query(Accounts).filter_by(id = account_id).one()

        if you.type == 'ARTIST' and account.type == 'VENUE':
            text = you.username + ' canceled performing at your event'

        if you.type == 'VENUE' and account.type == 'ARTIST':
            text = you.username + ' canceled booking you for their event'

        new_notification = Notifications(action = ACTION_TYPES['CANCEL_BOOKING_REQUEST'],
            target_type = TARGET_TYPES['EVENT'], target_id = booking.event_rel.id,
            from_id = your_id, account_id = account_id,
            message = text, link = '/event/' + str(booking.event_rel.id))

        db_session.add(new_notification)

        sse.publish({"message": text, "for_id": account_id}, type='action')


        db_session.delete(booking)

        # commit everything: booking request and notification

        db_session.commit()

        return jsonify(message = 'booking request canceled!')


    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')



def cancel_booking_request(request, sse, event_id, receiver_id):
    try:
        # check given data

        your_id = user_session['account_id']

        if receiver_id == your_id:
            return jsonify(error = True, message = 'forbidden: provided account_id is equal to current account_id')

        event = db_session.query(Events).filter_by(id = event_id).first()
        if event == None:
            return jsonify(error = True, message = 'no event found by id: ' + str(event_id))

        if event.host_id != your_id and event.host_id != receiver_id:
            return jsonify(error = True, message = 'none of the two accounts own this event')


        # check if booking request already exists and if current session was the sender

        booking_request = db_session.query(EventRequests) \
        .filter(EventRequests.event_id == event_id) \
        .filter( (EventRequests.sender_id == your_id) | (EventRequests.receiver_id == your_id) ) \
        .filter( (EventRequests.sender_id == receiver_id) | (EventRequests.receiver_id == receiver_id) ) \
        .first()

        if not booking_request:
            response = '''Booking request does not exist.'''
            return jsonify(error = True, message = response,
            booking_request_exists = False)


        if booking_request.sender_id != your_id:
            response = '''You cannot cancel this booking request
            because you are not the sender.
            You must go to your requests page and either accept or decline.'''
            return jsonify(error = True, message = response,
            booking_request_exists = False)


        # delete booking request and old notification

        db_session.delete(booking_request)

        check_notification = db_session.query(Notifications) \
        .filter(Notifications.action == ACTION_TYPES['REQUEST_BOOKING']) \
        .filter(Notifications.target_type == TARGET_TYPES['EVENT']) \
        .filter(Notifications.target_id == event_id) \
        .filter(Notifications.from_id == your_id) \
        .filter(Notifications.account_id == receiver_id) \
        .first()

        if check_notification:
            db_session.delete(check_notification)


        # create notification / push event

        if receiver_id != your_id:
            you = db_session.query(Accounts).filter_by(id = your_id).one()
            account = db_session.query(Accounts).filter_by(id = receiver_id).one()

            if you.type == 'ARTIST' and account.type == 'VENUE':
                text = you.username + ' canceled performing at your event'

            if you.type == 'VENUE' and account.type == 'ARTIST':
                text = you.username + ' canceled booking you for their event'

            new_notification = Notifications(action = ACTION_TYPES['CANCEL_BOOKING_REQUEST'],
                target_type = TARGET_TYPES['EVENT'], target_id = event.id,
                from_id = your_id, account_id = receiver_id,
                message = text, link = '/event/' + str(event.id))

            db_session.add(new_notification)

            sse.publish({"message": text, "for_id": receiver_id}, type='action')

        # commit everything: booking request and notification

        db_session.commit()

        return jsonify(message = 'booking request canceled!')


    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')



def decline_booking_request(request, sse, event_id, sender_id):
    try:
        # check given data

        your_id = user_session['account_id']
        if your_id == sender_id:
            response = '''sender_id is same as current session\'s id.
            The sender cannot accept/decline a request, only withdraw a request they sent'''
            return jsonify(error = True, message = response)


        event = db_session.query(Events).filter_by(id = event_id).first()
        if event == None:
            return jsonify(error = True, message = 'no event found by id: ' + str(event_id))

        if event.host_id != your_id and event.host_id != sender_id:
            return jsonify(error = True, message = 'none of the two accounts own this event')


        booking_request = db_session.query(EventRequests) \
        .filter(EventRequests.event_id == event_id) \
        .filter(EventRequests.sender_id == sender_id) \
        .filter(EventRequests.receiver_id == your_id) \
        .first()


        if not booking_request:
            response = '''booking request does not exist.
            maybe it was withdrawn by sender'''
            return jsonify(error = True, message = response, booking_request = False)


        db_session.delete(booking_request)

        if your_id != sender_id:
            you = db_session.query(Accounts).filter_by(id = your_id).one()

            text = you.username + ' declined your request to perform at event'

            new_notification = Notifications(action = ACTION_TYPES['BOOKED'],
                target_type = TARGET_TYPES['ACCOUNT'], target_id = sender_id,
                from_id = your_id, account_id = sender_id,
                message = text, link = '/event/' + str(event.id))

            db_session.add(new_notification)

            sse.publish({"message": text, "for_id": sender_id}, type='action')

        # commit everything: booking request and notification

        db_session.commit()

        return jsonify(message = 'request declined', booking = False)



    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')

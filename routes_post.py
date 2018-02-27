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
from models import Conversations, ConversationMessages, Messages

import chamber
from chamber import uniqueValue
from chamber import ARTIST_EVENT_STATUSES, ACTION_TYPES, TARGET_TYPES, ERROR_TYPES




def logged_in():
    return 'session_id' in user_session and 'account_id' in user_session
# ---





def signup(request, sse):
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
        user_session['account_type']   = new_account.type

        return jsonify(account = new_account.serialize, message = 'Signed Up!')

    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error signing up...')




def create_event(request, sse):
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
        date_str          = str(request.form['date_str']).encode()
        date_concat       = str(request.form['date_concat']).encode()
        event_date        = datetime.strptime(date_str, '%Y-%m-%d')
        event_date_time   = datetime.strptime(date_concat, '%Y-%m-%d %H:%M:%S')

        new_event = Events(title = title, desc = desc, categories = categories, location = location,
                            link = link, event_date = event_date, event_date_time = event_date_time, host_id = you.id)

        message = you.username + ' created an event: ' + new_event.title

        if 'event_photo' not in request.files:
            db_session.add(new_event)
            db_session.commit()

            sse.publish({"message": message, "account_id": you.id}, type='notify')

            return jsonify(message = 'Event Created Successfully!', event = new_event.serialize)

        else:
            file = request.files['event_photo']
            if file and file.filename != '' and chamber.allowed_photo(file.filename):
                icon = chamber.uploadFile(file = file, prev_ref = '')

                new_event.icon = icon

                db_session.add(new_event)
                db_session.commit()

                sse.publish({"message": message, "account_id": you.id}, type='notify')

                return jsonify(message = 'Event Created Successfully!', event = new_event.serialize)

            else:
                return jsonify(error = True, message = 'file was not of type: image')


    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')



def toggle_event_like(request, sse, event_id):
    event = db_session.query(Events).filter_by(id = event_id).first()
    if not event:
        return jsonify(error = True, message = 'event not found')

    like = db_session.query(EventLikes) \
    .filter_by(event_id = event_id) \
    .filter_by(owner_id = user_session['account_id']) \
    .first()

    if like:
        db_session.delete(like)

        check_notification = db_session.query(Notifications) \
        .filter(Notifications.action == ACTION_TYPES['EVENT_LIKE']) \
        .filter(Notifications.target_type == TARGET_TYPES['EVENT']) \
        .filter(Notifications.target_id == like.event_id) \
        .filter(Notifications.from_id == user_session['account_id']) \
        .filter(Notifications.account_id == like.event_rel.host_id) \
        .first()

        if check_notification:
            db_session.delete(check_notification)

        db_session.commit()

        return jsonify(message = 'unliked', liked = False)

    else:
        like = EventLikes(event_id = event_id, owner_id = user_session['account_id'])
        db_session.add(like)
        db_session.commit()

        if like.event_rel.host_id != user_session['account_id']:
            you = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()

            message = you.username + ' liked your event: ' + like.event_rel.title

            new_notification = Notifications(action = ACTION_TYPES['EVENT_LIKE'],
                target_type = TARGET_TYPES['EVENT'], target_id = like.event_id ,
                from_id = user_session['account_id'], account_id = like.event_rel.host_id,
                message = message, link = '/event/' + str(event_id))

            db_session.add(new_notification)
            db_session.commit()

            sse.publish({"message": message, "for_id": like.event_rel.host_id}, type='action')

        return jsonify(message = 'liked', liked = True)



def toggle_event_attending(request, sse, event_id):
    if user_session['account_type'] != 'USER':
        return jsonify(error = True, message = 'current account is not of type: USER')

    event = db_session.query(Events).filter_by(id = event_id).first()
    if not event:
        return jsonify(error = True, message = 'event not found')

    attending = db_session.query(EventAttendees) \
    .filter_by(event_id = event_id) \
    .filter_by(account_id = user_session['account_id']) \
    .first()

    if attending:
        db_session.delete(attending)

        check_notification = db_session.query(Notifications) \
        .filter(Notifications.action == ACTION_TYPES['EVENT_ATTENDING']) \
        .filter(Notifications.target_type == TARGET_TYPES['EVENT']) \
        .filter(Notifications.target_id == attending.event_id) \
        .filter(Notifications.from_id == user_session['account_id']) \
        .filter(Notifications.account_id == attending.event_rel.host_id) \
        .first()

        if check_notification:
            db_session.delete(check_notification)

        db_session.commit()

        return jsonify(message = 'not attending', attending = False)

    else:
        attending = EventAttendees(event_id = event_id, account_id = user_session['account_id'])
        db_session.add(attending)
        db_session.commit()

        if attending.event_rel.host_id != user_session['account_id']:
            you = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()

            message = you.username + ' is attending your event: ' + attending.event_rel.title

            new_notification = Notifications(action = ACTION_TYPES['EVENT_ATTENDING'],
                target_type = TARGET_TYPES['EVENT'], target_id = attending.event_id ,
                from_id = user_session['account_id'], account_id = attending.event_rel.host_id,
                message = message, link = '/event/' + str(event_id))

            db_session.add(new_notification)
            db_session.commit()

            sse.publish({"message": message, "for_id": attending.event_rel.host_id}, type='action')

        return jsonify(message = 'attending', attending = True)


def toggle_comment_like(request, sse, comment_id):
    comment = db_session.query(EventComments).filter_by(id = comment_id).first()
    if not comment:
        return jsonify(error = True, message = 'comment not found')

    like = db_session.query(CommentLikes) \
    .filter_by(comment_id = comment_id) \
    .filter_by(owner_id = user_session['account_id']) \
    .first()

    if like:
        db_session.delete(like)

        check_notification = db_session.query(Notifications) \
        .filter(Notifications.action == ACTION_TYPES['COMMENT_LIKE']) \
        .filter(Notifications.target_type == TARGET_TYPES['COMMENT']) \
        .filter(Notifications.target_id == like.comment_id) \
        .filter(Notifications.from_id == user_session['account_id']) \
        .filter(Notifications.account_id == like.comment_rel.owner_id) \
        .first()

        if check_notification:
            db_session.delete(check_notification)

        db_session.commit()

        return jsonify(message = 'unliked', liked = False)

    else:
        like = CommentLikes(comment_id = comment_id, owner_id = user_session['account_id'])
        db_session.add(like)
        db_session.commit()

        if like.comment_rel.owner_id != user_session['account_id']:
            you = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()

            message = you.username + ' liked your comment: ' + like.comment_rel.text

            new_notification = Notifications(action = ACTION_TYPES['COMMENT_LIKE'],
                target_type = TARGET_TYPES['COMMENT'], target_id = like.comment_id,
                from_id = user_session['account_id'], account_id = like.comment_rel.owner_id,
                message = message, link = '/event/' + str(like.comment_rel.event_rel.id))

            db_session.add(new_notification)
            db_session.commit()

            sse.publish({"message": message, "for_id": like.comment_rel.owner_id}, type='action')

        return jsonify(message = 'liked', liked = True)



def toggle_account_follow(request, sse, account_id):
    account = db_session.query(Accounts).filter_by(id = account_id).first()
    if not account:
        return jsonify(error = True, message = 'account not found')

    if account_id == user_session['account_id']:
        return jsonify(error = True, message = 'provided account_id is same as session account\'s id: accounts cannot follow themselves.')

    follow = db_session.query(Follows) \
    .filter_by(account_id = user_session['account_id']) \
    .filter_by(follows_id = account_id) \
    .first()

    if follow:
        db_session.delete(follow)

        check_notification = db_session.query(Notifications) \
        .filter(Notifications.action == ACTION_TYPES['ACCOUNT_FOLLOW']) \
        .filter(Notifications.target_type == TARGET_TYPES['ACCOUNT']) \
        .filter(Notifications.target_id == account_id) \
        .filter(Notifications.from_id == user_session['account_id']) \
        .filter(Notifications.account_id == account_id) \
        .first()

        if check_notification:
            db_session.delete(check_notification)

        db_session.commit()

        return jsonify(message = 'unfollowed', following = False)

    else:
        follow = Follows(account_id = user_session['account_id'], follows_id = account_id)
        db_session.add(follow)

        if account_id != user_session['account_id']:
            you = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()

            message = you.username + ' started following you'

            new_notification = Notifications(action = ACTION_TYPES['ACCOUNT_FOLLOW'],
                target_type = TARGET_TYPES['ACCOUNT'], target_id = account_id,
                from_id = user_session['account_id'], account_id = account_id,
                message = message)

            db_session.add(new_notification)

            sse.publish({"message": message, "for_id": account_id}, type='action')

        db_session.commit()

        return jsonify(message = 'followed', following = True)



def create_event_comment(request, sse, event_id):
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

    if event.host_id != user_session['account_id']:
        you = db_session.query(Accounts).filter_by(id = user_session['account_id']).one()

        message = you.username + ' commented on your event(' + event.title[:10] + '...' + '): ' + text[:10] + '...'

        new_notification = Notifications(action = ACTION_TYPES['NEW_COMMENT'],
            target_type = TARGET_TYPES['EVENT'], target_id = event.id,
            from_id = user_session['account_id'], account_id = event.host_id,
            message = message, link = '/event/' + str(event.id))

        db_session.add(new_notification)

        sse.publish({"message": message, "for_id": event.host_id}, type='action')

    db_session.commit()

    return jsonify(message = 'event comment created', comment = new_comment.serialize)



def send_account_message(request, sse, account_id):
    try:
        your_id = user_session['account_id']

        if account_id == your_id:
            return jsonify(error = True, message = 'account_id provided is same as current user.')

        data = json.loads(request.data)
        if not data:
            return jsonify( error = True, message = 'request body is empty, check headers/data' )
        if 'message' not in data:
            return jsonify( error = True, message = 'no message key/value pair in request body' )


        conversation = db_session.query(Conversations) \
        .filter( (Conversations.account_A_id == your_id) | (Conversations.account_B_id == your_id) ) \
        .filter( (Conversations.account_A_id == account_id) | (Conversations.account_B_id == account_id) ) \
        .first()

        if conversation == None:
            conversation = Conversations(account_A_id = your_id, account_B_id = account_id)
            db_session.add(conversation)
            db_session.commit()

        conversation.last_updated = func.now()
        db_session.add(conversation)

        message = str(data['message']).encode()
        conversation_messge = ConversationMessages(conversation_id = conversation.id, owner_id = your_id, message = message)
        db_session.add(conversation_messge)

        if account_id != your_id:
            you = db_session.query(Accounts).filter_by(id = your_id).one()

            text = you.username + ' sent you a message'

            new_notification = Notifications(action = ACTION_TYPES['NEW_MESSAGE'],
                target_type = TARGET_TYPES['ACCOUNT'], target_id = account_id,
                from_id = your_id, account_id = account_id,
                message = text, link = '/accounts/' + str(you.username))

            db_session.add(new_notification)

            sse.publish({"message": text, "for_id": account_id}, type='action')

        db_session.commit()

        sse.publish({"message": text, "conversation_message": conversation_messge.serialize}, type='message')

        return jsonify(message = 'message sent', new_message = conversation_messge.serialize)


    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')



def send_booking_request(request, sse, event_id, account_id):
    try:
        # check given data

        your_id = user_session['account_id']

        if account_id == your_id:
            return jsonify(error = True, message = 'forbidden: provided account_id is equal to current account_id')

        event = db_session.query(Events).filter_by(id = event_id).first()
        if event == None:
            return jsonify(error = True, message = 'no event found by id: ' + str(event_id))

        if event.host_id != your_id and event.host_id != account_id:
            return jsonify(error = True, message = 'none of the two accounts own this event')


        # check if booking request and notification already exists

        booking_request = db_session.query(EventRequests) \
        .filter(EventRequests.event_id == event_id) \
        .filter( (EventRequests.sender_id == your_id) | (EventRequests.receiver_id == your_id) ) \
        .filter( (EventRequests.sender_id == account_id) | (EventRequests.receiver_id == account_id) ) \
        .first()

        if booking_request:
            response = '''Booking request already exists.'''
            return jsonify(error = True, message = response,
            booking_request_exists = True, booking_request = booking_request.serialize)

        check_notification = db_session.query(Notifications) \
        .filter(Notifications.action == ACTION_TYPES['REMOVE_BOOKING']) \
        .filter(Notifications.target_type == TARGET_TYPES['EVENT']) \
        .filter(Notifications.target_id == event_id) \
        .filter(Notifications.from_id == your_id) \
        .filter(Notifications.account_id == account_id) \
        .first()

        if check_notification:
            db_session.delete(check_notification)


        # create booking request

        new_booking_request = EventRequests(sender_id = your_id, receiver_id = account_id, event_id = event_id)
        db_session.add(new_booking_request)


        # create notification / push event

        if account_id != your_id:
            you = db_session.query(Accounts).filter_by(id = your_id).one()
            account = db_session.query(Accounts).filter_by(id = account_id).one()

            if you.type == 'ARTIST' and account.type == 'VENUE':
                text = you.username + ' wants to perform at your event: ' + event.title

            if you.type == 'VENUE' and account.type == 'ARTIST':
                text = you.username + ' wants you to perform at their event: ' + event.title

            new_notification = Notifications(action = ACTION_TYPES['REQUEST_BOOKING'],
                target_type = TARGET_TYPES['EVENT'], target_id = event.id,
                from_id = your_id, account_id = account_id,
                message = text, link = '/event/' + str(event.id))

            db_session.add(new_notification)

            sse.publish({"message": text, "for_id": account_id}, type='action')

        # commit everything: booking request and notification

        db_session.commit()

        return jsonify(message = 'booking request sent!', new_booking_request = new_booking_request.serialize)


    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')



def cancel_booking_request(request, sse, event_id, account_id):
    try:
        # check given data

        your_id = user_session['account_id']

        if account_id == your_id:
            return jsonify(error = True, message = 'forbidden: provided account_id is equal to current account_id')

        event = db_session.query(Events).filter_by(id = event_id).first()
        if event == None:
            return jsonify(error = True, message = 'no event found by id: ' + str(event_id))

        if event.host_id != your_id and event.host_id != account_id:
            return jsonify(error = True, message = 'none of the two accounts own this event')


        # check if booking request already exists and if current session was the sender

        booking_request = db_session.query(EventRequests) \
        .filter(EventRequests.event_id == event_id) \
        .filter( (EventRequests.sender_id == your_id) | (EventRequests.receiver_id == your_id) ) \
        .filter( (EventRequests.sender_id == account_id) | (EventRequests.receiver_id == account_id) ) \
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
        .filter(Notifications.account_id == account_id) \
        .first()

        if check_notification:
            db_session.delete(check_notification)


        # create notification / push event

        if account_id != your_id:
            you = db_session.query(Accounts).filter_by(id = your_id).one()
            account = db_session.query(Accounts).filter_by(id = account_id).one()

            if you.type == 'ARTIST' and account.type == 'VENUE':
                text = you.username + ' canceled performing at your event: ' + event.title

            if you.type == 'VENUE' and account.type == 'ARTIST':
                text = you.username + ' canceled booking you for their event: ' + event.title

            new_notification = Notifications(action = ACTION_TYPES['REMOVE_BOOKING'],
                target_type = TARGET_TYPES['EVENT'], target_id = event.id,
                from_id = your_id, account_id = account_id,
                message = text, link = '/event/' + str(event.id))

            db_session.add(new_notification)

            sse.publish({"message": text, "for_id": account_id}, type='action')

        # commit everything: booking request and notification

        db_session.commit()

        return jsonify(message = 'booking request canceled!')


    except Exception as err:
        print(err)
        return jsonify(error = True, errorMessage = str(err), message = 'error processing...')

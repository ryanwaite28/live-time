import os , sys , cgi , re, hmac, hashlib, smtplib, requests, datetime
import logging, dateutil, sqlite3, urllib, httplib2, json, psycopg2
import random, string

from werkzeug.utils import secure_filename

import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage




current_dir = os.path.dirname(os.path.abspath(__file__))
firebase_json_file_dir = os.path.join( current_dir , 'firebase.json' )

config = {
    'apiKey': "AIzaSyAQL_V6IejrtuGmav9VPWKb-Ll0GBU-oQc",
    'authDomain': "live-time.firebaseapp.com",
    'databaseURL': "https://live-time.firebaseio.com",
    'projectId': "live-time",
    'storageBucket': "live-time.appspot.com",
    'messagingSenderId': "1003960112164",

    "serviceAccount": firebase_json_file_dir
}

firebase = pyrebase.initialize_app(config)
cred = credentials.Certificate(firebase_json_file_dir)
firebase_admin.initialize_app(cred, {
    'storageBucket': config['storageBucket']
})



def sendMSG(email, subject, msg):
    # Set Headers

    FROM = "status@travellrs.com"
    TO = [email] # must be a list
    SUBJECT = subject
    TEXT = msg

    # Prepare actual message

    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    try:
        server = smtplib.SMTP('mail.travellrs.com:25')
        server.starttls()
        server.login('status@travellrs.com', 'RMW@nasa2015')
        server.sendmail(FROM, TO, message)
        server.quit()

        return 'successful'

    except Exception:
        return 'unsuccessful'

# ---

def newUserAlert():
    # Set Headers

    FROM = "status@travellrs.com"
    TO = ["ryanwaite28@gmail.com"] # must be a list
    SUBJECT = 'New User!'
    TEXT = 'New User Joined!!!'

    # Prepare actual message

    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)


    server = smtplib.SMTP('mail.travellrs.com:25')
    server.starttls()
    server.login('status@travellrs.com', 'RMW@nasa2015')
    server.sendmail(FROM, TO, message)
    server.quit()

# ---

def errorAlert(msg):

    if not msg:
        msg = ''

    # Set Headers

    FROM = "status@travellrs.com"
    TO = ["ryanwaite28@gmail.com"] # must be a list
    SUBJECT = 'Error Alert.'
    TEXT = msg

    # Prepare actual message

    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)


    server = smtplib.SMTP('mail.travellrs.com:25')
    server.starttls()
    server.login('status@travellrs.com', 'RMW@nasa2015')
    server.sendmail(FROM, TO, message)
    server.quit()

# ---

def uniqueValue():
    value = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(50))
    return value.lower()
# ---

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'])
ALLOWED_PHOTOS = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_VIDEOS = set(['mp4'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def allowed_photo(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_PHOTOS

def allowed_video(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_VIDEOS




def uploadFile(file, prev_ref):
    prev = str(prev_ref).encode()

    # print("prev --- ", prev)
    # print("string type --- ", type(prev) == str)
    # print("not empty --- ", prev != '')
    # print("has valid filename --- ", allowed_photo(prev))

    filename = uniqueValue() + secure_filename(file.filename)
    filepath = os.path.join( current_dir , filename )
    file.save( filepath )

    storage = firebase.storage()

    if prev and type(prev) == str and prev != '' and allowed_photo(prev):
        try:
            storage.delete(prev)
        except Exception:
            print("could not delete prev --- ", prev)
            # pass

    storage.child(filename).put(filepath)
    link = 'https://firebasestorage.googleapis.com/v0/b/' + config['storageBucket'] + '/o/' + filename + '?alt=media&token=None'


    os.remove( filepath )

    return link

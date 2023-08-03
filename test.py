import logging
from flask import Flask, request, render_template, flash, get_flashed_messages, redirect, url_for, jsonify
import colorlog
from colorama import Fore
import datetime
import pyrebase
import sys
sys.path.append("Report_generation")
from Report_generation.Forms import CreateUserForm
from customer_support.ticket import *
from imageUploader import FirebaseStorageClient
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from Report_generation.report_class import Com_Report, Indi_Report, Trans_Report
from Report_generation.Admin_classes import *
from Report_generation.report_functions import get_all_reports, retrieve_report_name, retrieve_ByID
from Report_generation.report_functions import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from flask_socketio import SocketIO, send




config = {
    "apiKey": load_dotenv("PYREBASE_API_TOKEN"),
    "authDomain": "kaki-db097.firebaseapp.com",
    "projectId": "kaki-db097",
    "databaseURL": "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "kaki-db097.appspot.com",
}

cred = credentials.Certificate('Account_management/credentials.json')
firebase_admin.initialize_app(cred, {'databaseURL': "https://kaki-db097-default-rtdb.asia-southeast1.firebasedatabase.app/"})


app = Flask(__name__)
app.secret_key = 'karthik123'
socketio = SocketIO(app)
current_user = 'Leap'


app.config['UPLOAD_FOLDER'] = "/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

firebase = pyrebase.initialize_app(config)
pyredb = firebase.database()
pyreauth = firebase.auth()
pyrestorage = firebase.storage()


def getComments(): 
    comment = pyredb.child("comments").get()
    return comment



if __name__ == "__main__": 
    print(getComments())
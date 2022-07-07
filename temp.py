from __future__ import print_function

import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import Flask, render_template

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2 import service_account

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    result = json.loads(output) #this converts the json output to a python dictionary
    location = list(result.values()) # Printing the new dictionary
    print(location)#this shows the json converted as a python dictionary

    route = [[0, 2, 1, 0], [0, 3, 0]]
    route =jsonify(route)
#    print("HI")
    print(route)
    return route
#    return render_template('map.html')    


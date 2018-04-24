from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


import pyrebase
import git
import sys
import os.path
sys.path.append(os.path.abspath("../diafano-vault/"))

credentials_file = "../diafano-vault/credentials.py"

if not os.path.isfile(credentials_file):
    git.Git("../").clone("https://github.com/mertaytore/diafano-vault.git")

# import credentials for firebase
from credentials import export_credentials
config = export_credentials(None)

firebase_config = config['firebaseConfig']

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
database = firebase.database()

def landing(request):
    return render(request,"landing.html", {"mapbox_access_token" : config['mapboxgl']['accessToken']})

def signIn(request):
    return render(request,"signIn.html", {"mapbox_access_token" : config['mapboxgl']['accessToken']})

def signUp(request):
    return render(request,"signup.html", {"mapbox_access_token" : config['mapboxgl']['accessToken']})

def dashboard(request):
    return render(request,"dashboard.html", {"mapbox_access_token" : config['mapboxgl']['accessToken']})

def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'log.html')

def postsignup(request):
    name = request.POST.get('username')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = auth.create_user_with_email_and_password(email, passw)
        uid = user['localId']
    except:
        message = "Unable to create account try again"
        return render(request, "signup.html", { "messg" : message })
        uid = user['localId']

    location = {
        "latitude" : -1,
        "long" : -1
    }

    data = {
        "bio" : "",
        "email" : email,
        "location" : location,
        "location_share" : "False",
        "name" : "",
        "phone_number" : "-1",
        "profile_picture" : "",
        "trust_rank" : 0
    }

    database.child("users").child(name).set(data)

    # this will be redirecting to settings & dashboard
    return render(request,"dashboard.html", {"mapbox_access_token" : config['mapboxgl']['accessToken']})

def postsignup_google(request):
    current_user = request.user
    print(current_user.email)
    name = current_user.username
    email = current_user.email
    passw = current_user.email

    try:
        user = auth.create_user_with_email_and_password(email, passw)
        uid = user['localId']
    except:
        message = "Unable to create account try again"
        return render(request, "signup.html", { "messg" : message })
        uid = user['localId']

    location = {
        "latitude" : -1,
        "long" : -1
    }

    data = {
        "bio" : "",
        "email" : email,
        "location" : location,
        "location_share" : "False",
        "name" : "",
        "phone_number" : "-1",
        "profile_picture" : "",
        "trust_rank" : 0
    }

    database.child("users").child(name).set(data)

    # this will be redirecting to settings & dashboard
    return render(request,"dashboard.html", {"mapbox_access_token" : config['mapboxgl']['accessToken']})

from django.shortcuts import render
from django.http import HttpResponse

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
    return render(request,"signIn.html")

def signUp(request):
    return render(request,"signup.html")

def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = auth.create_user_with_email_and_password(email, passw)
        uid = user['localId']
    except:
        message = "Unable to create account try again"
        return render(request, "signup.html", { "messg" : message })
        uid = user['localId']

    data = { "name" : name, "status" : "1" }

    database.child("users").child(uid).child("details").set(data)
    return render(request,"signIn.html")

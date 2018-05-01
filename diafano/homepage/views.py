from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.views import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import pyrebase
import sys
import os.path
sys.path.append(os.path.abspath("../diafano-vault/"))

credentials_file = "diafano-vault/credentials.py"

# import credentials for firebase
from credentials import export_credentials
config = export_credentials(None)

firebase_config = config['firebaseConfig']

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
database = firebase.database()
storage = firebase.storage()

def landing(request):
    return render(request,"landing.html", {"mapbox_access_token" : config['mapboxgl']['accessToken']})

def logout(request):
    [sp.session.delete() for sp in SessionProfile.objects]
    logout(request)
    return landing(request)

def signIn(request):
    return render(request,"signIn.html", {"mapbox_access_token" : config['mapboxgl']['accessToken']})

def signUp(request):
    print(request.user.is_anonymous)
    if request.user.is_anonymous:
        return render(request,"signup.html", {"mapbox_access_token" : config['mapboxgl']['accessToken']})
    else:
        return render(request,"dashboard.html", {
            "firebase_apikey" : config['firebaseConfig']['apiKey'],
            "mapbox_access_token" : config['mapboxgl']['accessToken'],
            "firebase_authdomain" : config['firebaseConfig']['authDomain'],
            "firebase_dburl" : config['firebaseConfig']['databaseURL'],
            "firebase_storagebucket" : config['firebaseConfig']['storageBucket']})

def dashboard(request):
    return render(request,"dashboard.html", {
        "firebase_apikey" : config['firebaseConfig']['apiKey'],
        "mapbox_access_token" : config['mapboxgl']['accessToken'],
        "firebase_authdomain" : config['firebaseConfig']['authDomain'],
        "firebase_dburl" : config['firebaseConfig']['databaseURL'],
        "firebase_storagebucket" : config['firebaseConfig']['storageBucket']})

def postsignup(request):
    if request.user.is_anonymous:
        name = request.POST.get('name')
        email = request.POST.get('email')
        passw = request.POST.get('pass')
        try:
            user = auth.create_user_with_email_and_password(email, passw)
            uid = user['localId']
        except:
            message = "Unable to create account try again"
            return render(request, "landing.html", { "messg" : message, "mapbox_access_token" : config['mapboxgl']['accessToken'] })
            uid = user['localId']
        local_user = User.objects.create_user(email, email, passw)
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
            "profile_picture" : "https://firebasestorage.googleapis.com/v0/b\
            /diafano-d139c.appspot.com/o/profiledefault.png?alt=media&token=25d375c4-f233-442b-8c1b-1a7b5ab656df",
            "trust_rank" : 0
        }
        database.child("users").child(name).set(data)

        request.session['firebase_user'] = user
        request.session['username'] = username
        # this will be redirecting to settings & dashboard
        return render(request,"dashboard.html", {
            "firebase_apikey" : config['firebaseConfig']['apiKey'],
            "mapbox_access_token" : config['mapboxgl']['accessToken'],
            "firebase_authdomain" : config['firebaseConfig']['authDomain'],
            "firebase_dburl" : config['firebaseConfig']['databaseURL'],
            "firebase_storagebucket" : config['firebaseConfig']['storageBucket']})
    else:
        return render(request,"dashboard.html", {
            "firebase_apikey" : config['firebaseConfig']['apiKey'],
            "mapbox_access_token" : config['mapboxgl']['accessToken'],
            "firebase_authdomain" : config['firebaseConfig']['authDomain'],
            "firebase_dburl" : config['firebaseConfig']['databaseURL'],
            "firebase_storagebucket" : config['firebaseConfig']['storageBucket']})

def postsignup_google(request):
    if request.user.is_anonymous:
        current_user = request.user
        name = current_user.username
        email = current_user.email
        passw = current_user.email

        try:
            user = auth.create_user_with_email_and_password(email, passw)
            uid = user['localId']
        except:
            message = "Unable to create account try again"
            return render(request, "landing.html", { "messg" : message, "mapbox_access_token" : config['mapboxgl']['accessToken'] })
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
            "profile_picture" : "https://firebasestorage.googleapis.com/v0/b/diafano-d139c.appspot.com/o\
            /profiledefault.png?alt=media&token=25d375c4-f233-442b-8c1b-1a7b5ab656df",
            "trust_rank" : 0
        }

        database.child("users").child(name).set(data)
        request.session['firebase_user'] = user
        request.session['username'] = username
        # this will be redirecting to settings & dashboard
        return render(request,"dashboard.html", {
            "firebase_apikey" : config['firebaseConfig']['apiKey'],
            "mapbox_access_token" : config['mapboxgl']['accessToken'],
            "firebase_authdomain" : config['firebaseConfig']['authDomain'],
            "firebase_dburl" : config['firebaseConfig']['databaseURL'],
            "firebase_storagebucket" : config['firebaseConfig']['storageBucket']})
    return render(request,"dashboard.html", {
        "firebase_apikey" : config['firebaseConfig']['apiKey'],
        "mapbox_access_token" : config['mapboxgl']['accessToken'],
        "firebase_authdomain" : config['firebaseConfig']['authDomain'],
        "firebase_dburl" : config['firebaseConfig']['databaseURL'],
        "firebase_storagebucket" : config['firebaseConfig']['storageBucket']})


def postsignin(request):
    if request.user.is_anonymous:
        email = request.POST.get('username')
        passw = request.POST.get('pass')
        try:
            user = auth.sign_in_with_email_and_password(email, passw)
            if user is None:
                message = "Unable to sign in to account try again"
                return render(request, "landing.html", { "messg" : message, "mapbox_access_token" : config['mapboxgl']['accessToken'] })

            #uid = user['localId']
            local_user = authenticate(request, username=email, password=passw)
            if local_user is not None:
                if not local_user.is_active:
                    login(local_user)
            else:
                local_user = User.objects.create_user(email, email, passw)
            # Return an 'invalid login' error message.
            request.session['firebase_user'] = user
            request.session['username'] = username
            return render(request,"dashboard.html", {
                "firebase_apikey" : config['firebaseConfig']['apiKey'],
                "mapbox_access_token" : config['mapboxgl']['accessToken'],
                "firebase_authdomain" : config['firebaseConfig']['authDomain'],
                "firebase_dburl" : config['firebaseConfig']['databaseURL'],
                "firebase_storagebucket" : config['firebaseConfig']['storageBucket']})
        except:
            message = "Unable to sign in to account try again"
            return render(request, "landing.html", { "messg" : message, "mapbox_access_token" : config['mapboxgl']['accessToken'] })
    request.session['firebase_user'] = user
    request.session['username'] = username
    return render(request,"dashboard.html", {
        "firebase_apikey" : config['firebaseConfig']['apiKey'],
        "mapbox_access_token" : config['mapboxgl']['accessToken'],
        "firebase_authdomain" : config['firebaseConfig']['authDomain'],
        "firebase_dburl" : config['firebaseConfig']['databaseURL'],
        "firebase_storagebucket" : config['firebaseConfig']['storageBucket']})

def postsignin_google(request):

    current_user = request.user
    name = current_user.username
    email = current_user.email
    passw = current_user.email

    try:
        user = auth.sign_in_with_email_and_password(email, passw)
        uid = user['localId']
        request.session['username'] = name
        request.session['firebase_user'] = user['idToken']
        request.session['username'] = username
        return render(request,"dashboard.html", {
            "firebase_apikey" : config['firebaseConfig']['apiKey'],
            "mapbox_access_token" : config['mapboxgl']['accessToken'],
            "firebase_authdomain" : config['firebaseConfig']['authDomain'],
            "firebase_dburl" : config['firebaseConfig']['databaseURL'],
            "firebase_storagebucket" : config['firebaseConfig']['storageBucket']})
    except:
        message = "Unable to sign in to account try again"
        return render(request, "landing.html", { "messg" : message, "mapbox_access_token" : config['mapboxgl']['accessToken'] })


@login_required
def user_settings(request):
    user = auth.get_account_info(request.session["firebase_user"])

    email  = user['users'][0]['providerUserInfo'][0]["email"]
    users_by_email = database.child("users").order_by_child("email").equal_to(email).get().val()

    users_by_email = dict(users_by_email)
    username = list(users_by_email)[0]
    users_by_email = users_by_email[username]
    
    return render(request, "settings.html", {"username": username, "email": users_by_email['email'],
    "bio": users_by_email['bio'], "profile_picture": users_by_email['profile_picture'],
    "phone_number": users_by_email['phone_number'],
    "firebase_apikey" : config['firebaseConfig']['apiKey'],
    "mapbox_access_token" : config['mapboxgl']['accessToken'],
    "firebase_authdomain" : config['firebaseConfig']['authDomain'],
    "firebase_dburl" : config['firebaseConfig']['databaseURL'],
    "firebase_storagebucket" : config['firebaseConfig']['storageBucket']})

@login_required
def update_user_settings(request):
    user = auth.get_account_info(request.session["firebase_user"])
    
    key = request.POST.get('key')
    value = request.POST.get('value')

    email  = user['users'][0]['providerUserInfo'][0]["email"]
    users_by_email = database.child("users").order_by_child("email").equal_to(email).get().val()
    users_by_email = dict(users_by_email)
    username = list(users_by_email)[0]
    users_by_email = users_by_email[username]
    database.child("users").child(username).child(key).set(value)

    return redirect("/settings/", {"username": username, "email": users_by_email['email'],
    "bio": users_by_email['bio'], "profile_picture": users_by_email['profile_picture'],
    "phone_number": users_by_email['phone_number'],
    "firebase_apikey" : config['firebaseConfig']['apiKey'],
    "mapbox_access_token" : config['mapboxgl']['accessToken'],
    "firebase_authdomain" : config['firebaseConfig']['authDomain'],
    "firebase_dburl" : config['firebaseConfig']['databaseURL'],
    "firebase_storagebucket" : config['firebaseConfig']['storageBucket']})

@login_required
def update_pic(request):
    user = auth.get_account_info(request.session["firebase_user"])
   
    key = request.POST.get('key')
    value = request.POST.get('value')

    email  = user['users'][0]['providerUserInfo'][0]["email"]
    users_by_email = database.child("users").order_by_child("email").equal_to(email).get().val()
    users_by_email = dict(users_by_email)
    username = list(users_by_email)[0]
    users_by_email = users_by_email[username]

    pic_name = username + ".jpg"
    storage.child(pic_name).put(request.FILES['pic'])
    path_to_pic = storage.child(pic_name).get_url(request.session["firebase_user"])
    database.child("users").child(username).child("profile_picture").set(path_to_pic)
    # database.child("users").child(username).child(key).set(value)

    return redirect("/settings/", {"username": username, "email": users_by_email['email'],
    "bio": users_by_email['bio'], "profile_picture": users_by_email['profile_picture'],
    "phone_number": users_by_email['phone_number'],
    "firebase_apikey" : config['firebaseConfig']['apiKey'],
    "mapbox_access_token" : config['mapboxgl']['accessToken'],
    "firebase_authdomain" : config['firebaseConfig']['authDomain'],
    "firebase_dburl" : config['firebaseConfig']['databaseURL'],
    "firebase_storagebucket" : config['firebaseConfig']['storageBucket']})

@login_required
def view_profile(request):
    if 'name' in request.GET and request.GET['name']:
        user = request.GET['name']
    else:
        return HttpResponse('Please submit a search term.')
    
    try:
        users_by_email = database.child("users").child(user).get().val()
    except:
        return HttpResponse('Enter a valid user name!.')
    
    users_by_email = dict(users_by_email)
    username = list(users_by_email)[0]
    
    return render(request, "profile.html", {"username": user, "email": users_by_email['email'],
    "bio": users_by_email['bio'], "profile_picture": users_by_email['profile_picture'],
    "phone_number": users_by_email['phone_number'],
    "firebase_apikey" : config['firebaseConfig']['apiKey'],
    "mapbox_access_token" : config['mapboxgl']['accessToken'],
    "firebase_authdomain" : config['firebaseConfig']['authDomain'],
    "firebase_dburl" : config['firebaseConfig']['databaseURL'],
    "firebase_storagebucket" : config['firebaseConfig']['storageBucket']})

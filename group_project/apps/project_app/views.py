from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from apps.project_app.models import User
import bcrypt
import argparse
import json
import pprint
import requests
import sys
import urllib

API_HOST = 'https://api.yelp.com'
URL = 'https://api.yelp.com/v3/businesses/search'
SEARCH_PATH = '/v3/businesses/search'
api_key = '8fJisUcWi6_6M8q1TqXwV64duaoO7p6rs5Sh4xI9b6abzOxLgAHFW_OrD2jgX7rRH0a2bwm4Uhio4-5JiVQCbTHyvrzs8667unV_strpWIR6xq-CLwuT5V-uBH3KW3Yx'
header = {'Authorization': 'Bearer ' + api_key}




def index(request):
    if 'id' not in request.session or request.session['id'] == None:
        return render(request, "project_app/index.html")
    else:
        return redirect('/wheel')

def validate_register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw_hash,
        )
        user = User.objects.get(email=request.POST['email'])
        request.session['id'] = user.id
        request.session['message'] = "registered"
        return redirect("/login_success")

def validate_login(request):
    request.session['error'] = ""
    try:
        User.objects.get(email=request.POST['login_email'])
    except:
        request.session['error'] += "Incorrect Email"
        return redirect("/")
    user = User.objects.get(email=request.POST['login_email'])
    if user:
        if bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode()):
            request.session['message'] = "logged in"
            request.session['id'] = user.id
            return redirect("/wheel")
        else:
            request.session['error'] += "Incorrect Password"
            return redirect("/")

def wheel(request):
    return render(request, "project_app/wheel.html")

def process_wheel(request):
    return redirect("/results")

def preferences(request):
    return render(request, "project_app/preferences.html")

def process_preferences(request):
    request.session['category'] = request.POST['category']
    request.session['price'] = request.POST['price']
    request.session['city'] = request.POST["city"]
    return redirect('/wheel')

def results(request):
    print(request.session['data'])
    return render(request, "project_app/testsubject.html")

def success(request):
    data = User.objects.get(id=request.session['id'])
    userdict = {
        "datakey": data
    }
    return render(request, "project_app/success.html", userdict)

def logout(request):
    request.session['id'] = None
    return redirect('/')

def yelpAPI(request):
    category = 'term=chinese'
    location = 'location=Seattle'
    pricepoint = 'price=2'
    limit = 'limit=12'
    rating = 'sort_by=rating'
    response = requests.get(URL + '?{}&{}&{}&{}&{}'.format(category, location, pricepoint, limit, rating), headers = header)
    # request.session['business'] = response.json()
    business = response.json()
    result = json.dumps(business, sort_keys=True, indent=4)
    restdict = json.loads(result)
    print("*"*80)
    print(URL + '?{}&{}&{}&{}&{}'.format(category, location, pricepoint, limit, rating))
    print(result)
    print("*"*80)

    # business = request.session['business']

    # context = {
    #     'mileradius' : business['radius'],
    #     'location' : business['location'],
    #     'latitude': business['latitude'],
    #     'longitude': business['longitude'],
    #     'phone' : business['phone'],
    #     'url' : business['url'],
    #     'rating' : business[ 'rating'],
    #     'review_count' : business[ 'review_count'],
    #     'price' : business['price'],
    #     'name': business['name'],
    #     'categories': business['categories'],
    #     'is_cached': is_cached,
    #     'api_key': 'AIzaSyCX4x-GRqo8LUQQyYnCy6rgmC5PsefMtes',  # Don't do this! This is just an example. Secure your keys properly.\
    # }

    # return render(request, 'project_app/testsubject.html')
    return HttpResponse(result, content_type="application/json")

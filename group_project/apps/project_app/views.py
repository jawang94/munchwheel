from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from apps.project_app.models import User
from random import randint
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
        return redirect("/success")

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
    if 'category' not in request.session:
        request.session['category'] = "Restaurant"
    if 'price' not in request.session:
        request.session['price'] = "1,2,3,4"
    if 'city' not in request.session:
        request.session['city'] = "Seattle"
    if 'state' not in request.session:
        request.session['state'] = "WA"
    return render(request, "project_app/wheel.html")

def process_wheel(request):
    randnum = randint(0, 29)
    request.session['randnum'] = randnum
    return redirect("/results")

def preferences(request):
    if 'category' not in request.session:
        request.session['category'] = ""
    if 'price' not in request.session:
        request.session['price'] = ""
    if 'city' not in request.session:
        request.session['city'] = ""    
    if 'state' not in request.session:
        request.session['state'] = "" 
    if 'glutenfree' not in request.session:
        request.session['glutenfree'] = ""  
    if 'vegetarian' not in request.session:
        request.session['vegetarian'] = ""  
    if 'vegan' not in request.session:
        request.session['vegan'] = ""  
    return render(request, "project_app/preferences.html")

def process_preferences(request):
    request.session['category'] = request.POST["category"]
    request.session['price'] = request.POST["price"]
    request.session['city'] = request.POST["city"]
    request.session['state'] = request.POST["state"]
    return redirect('/wheel')

def process_advanced_preferences(request):
    if request.POST.get("gluten", False):
        request.session['glutenfree'] = ""
    else:
        request.session['glutenfree'] = "gluten free"
    
    if request.POST.get("vegetarian", False):
        request.session['vegetarian'] = ""
    else:
        request.session['vegetarian'] = "vegetarian"
    
    if request.POST.get("vegan", False):
        request.session['vegan'] = ""
    else:
        request.session['vegan'] = "vegan"
    return redirect('/preferences')

def results(request):
    google_api = 'AIzaSyCX4x-GRqo8LUQQyYnCy6rgmC5PsefMtes'
    x = 8000
    category = f'term={request.session["category"]},{request.session["glutenfree"]},{request.session["vegetarian"]},{request.session["vegan"]}'
    opennow = 'open_now=true'
    location = f'location={request.session["city"]},{request.session["state"]}'
    pricepoint = f'price={request.session["price"]}'
    limit = 'limit=30'
    rating = 'sort_by=rating'
    radius = f'radius={x}'
    attribute = f'attributes=hot_and_new'
    hotnew_term = ' term=restaurant'
    opennow = 'open_now=true'
    response = requests.get(URL + '?{}&{}&{}&{}&{}&{}&{}'.format(category, location, pricepoint, limit, rating, radius, opennow), headers = header)
    business = response.json()
    result = json.dumps(business, sort_keys=True, indent=4)
    restdict = json.loads(result)
###########################################################################################################################
    # this is top 10 restaurants in your area part
    response2 = requests.get(URL + '?{}&{}&{}&{}&{}&{}'.format(hotnew_term, location, limit, rating, radius, attribute), headers = header)
    business2 = response2.json()
    result2 = json.dumps(business2, sort_keys=True, indent=4)
    restdict2 = json.loads(result2)
    # end of top 10 restaurant part


    context = {
        'api_key' : google_api,
        'latitude' : restdict['businesses'][request.session['randnum']]['coordinates']['latitude'],
        'longitude' : restdict['businesses'][request.session['randnum']]['coordinates']['longitude'],

        # restaurant info stuff you need jason
        'restaurant_name' : restdict['businesses'][request.session['randnum']]['name'],
        # category (please loop this for all the categories 'titles' that exists) (this is an array btw)
        'title' : restdict['businesses'][request.session['randnum']]['categories'][0]['title'],
        'price' : restdict['businesses'][request.session['randnum']]['price'],
        'rating' : restdict['businesses'][request.session['randnum']]['rating'],
        'review_count' : restdict['businesses'][request.session['randnum']]['review_count'],
        #  address (please loop this for all lines of address that exists) (this is an array btw)
        'restaurant_address' : restdict['businesses'][request.session['randnum']]['location']['display_address'],
        'restaurant_url' : restdict['businesses'][request.session['randnum']]['url'],
        'restaurant_phone_number' : restdict['businesses'][request.session['randnum']]['display_phone'],
        'restaurant_image_url' : restdict['businesses'][request.session['randnum']]['image_url'],
############################################################################################################################
        # this is top 10 restaurants in your area part
        # 'restaurant_name2' : restdict2['businesses'][request.session[i]]['name'],
        # 'title2' : restdict2['businesses'][request.session[i]]['categories'][0]['title'],
        # 'price2' : restdict2['businesses'][request.session[i]]['price'],
        # 'rating2' : restdict2['businesses'][request.session[i]]['rating'],
        # 'review_count2' : restdict2['businesses'][request.session[i]]['review_count'],
        # 'restaurant_address2' : restdict2['businesses'][request.session[i]]['location']['display_address'],
        # 'restaurant_url2' : restdict2['businesses'][request.session[i]]['url'],
        # 'restaurant_phone_number2' : restdict2['businesses'][request.session[i]]['display_phone'],
        # end of top 10 restaurant part
    }
    print(request.session['vegetarian'])
    return render(request, "project_app/result.html", context)

def success(request):
    data = User.objects.get(id=request.session['id'])
    userdict = {
        "datakey": data
    }
    return render(request, "project_app/success.html", userdict)

def delete(request):
    request.session['glutenfree'] = ""
    request.session['vegitarian'] = ""
    request.session['vegan'] = ""
    return redirect('/preferences')

def logout(request):
    request.session['id'] = None
    return redirect('/')

from django.shortcuts import render
from django.views import View
import requests
import elasticsearch
from datetime import datetime
import random
import pandas as pd

def cleanSearch(data):
    array = []
    for x in data:
        x = x.get('_source')
        newArray = {
            "user": {
                "name": x.get('user').get('name'),
                "handle": x.get('user').get('screen_name'),
                "id": x.get('user').get('id'),
                "followers": x.get('user').get('followers_count'),
                "verified": x.get('user').get('verified'),
                "profile_image": x.get('user').get('profile_image_url')
            },
            "text": x.get('text'),
            "id": x.get('id_str'),
            "date": (datetime.strptime(x.get('created_at'), '%a %b %d %X %z %Y')).strftime("%b %d, %Y at %I:%M %p"),
            "favorites": x.get('retweet_count'),
            "retweets": x.get('favorite_count'),
        }
        array.append(newArray)
    return array

def getSite(link):
    sites = {'abc':'https://vignette.wikia.nocookie.net/logopedia/images/d/d7/Abc_2013_logo_dark_grey.svg/revision/latest/scale-to-width-down/200?cb=20180927202336',
             'cnn':'https://vignette.wikia.nocookie.net/logopedia/images/5/52/CNN_%282014%29.svg/revision/latest/scale-to-width-down/200?cb=20180509053533',
             'bbc':'https://vignette.wikia.nocookie.net/logopedia/images/e/eb/BBC.svg/revision/latest/scale-to-width-down/250?cb=20170913090831',
             'fox':'https://vignette.wikia.nocookie.net/logopedia/images/e/e9/FoxBCLogo2019.svg/revision/latest/scale-to-width-down/200?cb=20191121082502',
             'nyt':'https://vignette.wikia.nocookie.net/logopedia/images/d/d7/NYT_Masthead.svg/revision/latest/scale-to-width-down/250?cb=20141210032555',
             'washingtonpost':'https://vignette.wikia.nocookie.net/logopedia/images/c/c4/Washington-post-logo-thumb.jpg/revision/latest/scale-to-width-down/150?cb=20140719115207'}

    for site in sites.keys():
        if (link.count(site) > 0):
            return sites[site]

def cleanSearchNews(data):
    array = []
    for x in data:
        x = x.get('_source')
        newArray = {
            "summary": x.get('summary'),
            "title": x.get('title'),
            "link": x.get('link'),
            "logo": getSite(x.get('link')),
            "date": (pd.to_datetime(x.get('published'))).strftime("%b %d, %Y at %I:%M %p"),
        }
        array.append(newArray)
    return array


def searchTweets(term):
    es = elasticsearch.Elasticsearch([{'host': '167.71.250.175', 'port': 1371}])
    search_obj = {'query': {'bool': {'must': [{'match': {'tags': 'twitter'}}, {'wildcard': {'text': '* ' + term + ' *'}}]}}}
    data = es.search(index="filebeat-7.4.2-2019.12.10-000001", body=search_obj)["hits"]["hits"]
    return cleanSearch(data)


def searchNews(term):
    es = elasticsearch.Elasticsearch([{'host': '167.71.250.175', 'port': 1371}])
    search_obj = {'query': {'bool': {'must': [{'match': {'tags': 'news'}}, {'wildcard': {'title': '* ' + term + ' *'}}]}}}
    data = es.search(index="filebeat-7.4.2-2019.12.10-000001", body=search_obj)["hits"]["hits"]
    return cleanSearchNews(data)


def chooseRandom():
    topics = ["school", "test"]
    return random.choice(topics)


class HomePageView(View):
    def get(self, request, **kwargs):
        topic = chooseRandom()
        news, tweets = searchNews(topic), searchTweets(topic)
        return render(request, 'index.html', {"tweets": tweets, "news": news})

    def post(self, request):
        news, tweets = searchNews(request.POST["search"]), searchTweets(request.POST["search"])
        return render(request, 'index.html', {"tweets": tweets, "news": news})

class UserAccount(View):
    def get(self, request, **kwargs):
        data = None
        return render(request, 'useraccount.html', {"data":data})

class Main(View):
    def get(self, request, **kwargs):
        data = None
        return render(request, 'main.html', {"data":data})

class SignUp(View):
    def get(self, request, **kwargs):
        data = None
        return render(request, 'signup.html', {"data":data})

class Elastic(View):
    def get(self, request):
        return render(request, "elastic.html")

    def post(self, request):
        data = searchTweets(request.POST["search"])
        return render(request, "elastic.html", {"data": data})


from django.shortcuts import render
from django.views import View, generic
import requests
import elasticsearch
from datetime import datetime
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


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


def search(term):
    es = elasticsearch.Elasticsearch([{'host': '167.71.250.175', 'port': 1371}])
    search_obj = {'query': {'wildcard': {'text': '* ' + term + ' *'}}}
    data = es.search(index="filebeat-7.4.2-2019.11.13-000001", body=search_obj)["hits"]["hits"]
    return cleanSearch(data)

class HomePageView(View):
    def get(self, request, **kwargs):
        data = None
#         data = requests.get('elastic.html').json()
        # ignore above for now.
        return render(request, 'index.html', {"data": data})

    def post(self, request):
        data = search(request.POST["search"])
        return render(request, "index.html", {"data": data})


class UserAccount(View):
    def get(self, request, **kwargs):
        data = None
        return render(request, 'useraccount.html', {"data":data})

class Main(View):
    def get(self, request, **kwargs):
        data = None
#         data = requests.get('elastic.html').json()
        # ignore above for now.
        return render(request, 'registration/main.html', {"data": data})

    def post(self, request):
        data = search(request.POST["search"])
        return render(request, "regristration/main.html", {"data": data})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class Elastic(View):
    def get(self, request):
        return render(request, "elastic.html")

    def post(self, request):
        data = search(request.POST["search"])
        return render(request, "elastic.html", {"data": data})
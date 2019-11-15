from django.shortcuts import render
from django.views import View
import requests


def cleanSearch(data):
    array = []

    for x in data:
        source = x.get('_source')

        array.append(source)

    return array


def search(term):
    base_url = "http://167.71.250.175:1371/filebeat-7.4.2-2019.11.13-000001/_search?q=text:* "
    search_term = term
    req_url = base_url + search_term + " *"
    data = requests.get(req_url).json()["hits"]["hits"]

    print(req_url)
    return cleanSearch(data)

class HomePageView(View):
    def get(self, request, **kwargs):
        data = None
        # data = requests.get('elastic.html').json()
        # ignore above for now.
        return render(request, 'index.html', {"data": data})


class Elastic(View):
    def get(self, request):
        return render(request, "elastic.html")

    def post(self, request):
        data = search(request.POST["search"])
        return render(request, "elastic.html", {"data": data})


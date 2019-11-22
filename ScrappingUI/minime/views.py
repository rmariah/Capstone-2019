from django.shortcuts import render
from django.views import View
import requests
import elasticsearch


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
            "date": x.get('created_at'),
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
        # data = requests.get('elastic.html').json()
        # ignore above for now.
        return render(request, 'index.html', {"data": data})
    def post(self, request):
        data = search(request.POST["search"])
        return render(request, "index.html", {"data": data})


class Elastic(View):
    def get(self, request):
        return render(request, "elastic.html")

    def post(self, request):
        data = search(request.POST["search"])
        return render(request, "elastic.html", {"data": data})


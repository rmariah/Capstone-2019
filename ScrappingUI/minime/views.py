from django.shortcuts import render
from django.views import View

import requests


class HomePageView(View):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)


class Elastic(View):
    def get(self, request):
        # result = requests.get(your_link)
        print(result)
        return render(request, "elastic.html", {})


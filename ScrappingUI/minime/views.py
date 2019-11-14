from django.shortcuts import render
from django.views import View

class HomePageView(View):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)


class Elastic(View):
    def get(self, request):
        return render(request, "elastic.html", {})


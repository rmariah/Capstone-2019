from . import views
from django.conf.urls import url
from django.views.generic import RedirectView
from django.conf.urls import include, url

urlpatterns = [
    url(r'home/', views.HomePageView.as_view()),
    url('elastic/', views.Elastic.as_view()),
    url(r'useraccount/', views.UserAccount.as_view()),
]

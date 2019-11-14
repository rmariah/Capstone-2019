from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'home/', views.HomePageView.as_view()),
    url('elastic/', views.Elastic.as_view()),
]

from . import views
from django.conf.urls import url
from django.views.generic import RedirectView

urlpatterns = [
    url(r'home/', views.HomePageView.as_view()),
    url('elastic/', views.Elastic.as_view()),
    url(r'useraccount/', views.UserAccount.as_view()),
    url(r'logout/', RedirectView.as_view(url='account/logout')),
]

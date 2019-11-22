# howdy/urls.py
from minime import views

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
#     url(r'^$', views.HomePageView),
    url(r'^$', views.HomePageView.as_view()),
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += staticfiles_urlpatterns()
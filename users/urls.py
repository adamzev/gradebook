""" Users UrlConf """

from django.urls import include, path

urlpatterns = [
    # Auth urls: login, logout, password_change, password_change/done,
    # password_reset, password_reset/done, reset/<uidb64>/<token>, reset/done
    path('', include('django.contrib.auth.urls')),
]

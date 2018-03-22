""" Students UrlConf """

from django.urls import include, path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('new/', login_required(views.new_student), name='new_student'),
    path('', login_required(views.show_students), name='show_students'),
]

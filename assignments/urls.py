""" Assignments UrlConf """

from django.urls import include, path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('tasks/new/', login_required(views.new_task), name='new_task'),
    path('tasks/', login_required(views.show_tasks), name='show_tasks'),
]

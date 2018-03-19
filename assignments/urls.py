""" Assignments UrlConf """

from django.urls import include, path
from . import views

urlpatterns = [
    path('tasks/new/', views.new_task, name='new_task'),
    path('tasks/', views.show_tasks, name='show_tasks'),
]

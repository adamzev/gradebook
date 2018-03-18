""" Assignments UrlConf """

from django.urls import include, path
from . import views

urlpatterns = [
    path('new/', views.new_assignment, name='new_assignment'),
    path('', views.show_assignments, name='show_assignments'),
]

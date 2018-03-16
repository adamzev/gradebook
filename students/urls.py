""" Students UrlConf """

from django.urls import include, path
from . import views

urlpatterns = [
    path('new/', views.new_student, name='new_student'),
    path('', views.show_students, name='show_students'),
]

# from django.conf.urls import patterns, include, url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing),
    path('signup/', views.signUp, name = 'signup'),
    path('postsignup/', views.postsignup, name = 'postsignup'),
]

# from django.conf.urls import patterns, include, url
from django.urls import path, include
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from . import views

urlpatterns = [
    path('', views.landing),
    path('signup/', views.signUp, name = 'signup'),
    path('postsignup/', views.postsignup, name = 'postsignup'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='login'),
    #url(r'^logout/$', views.logout, name='logout'),
    url(r'^auth/', include('social_django.urls', namespace='social')),  # <- Here
    url(r'^$', views.home, name='home'),
]

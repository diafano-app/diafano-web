# from django.conf.urls import patterns, include, url
from django.urls import path, include
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.auth.views import logout
from . import views

urlpatterns = [
    path('', views.landing),
    path('signup/', views.signUp, name = 'signup'),
    path('signin/', views.signIn, name = 'signin'),
    path('postsignup/', views.postsignup, name = 'postsignup'),
    path('postsignin/', views.postsignin, name = 'postsignin'),
    path('postsignup_google/', views.postsignup_google, name = 'postsignup_google'),
    path('postsignin_google/', views.postsignin_google, name = 'postsignin_google'),
    path('settings/', views.user_settings, name = 'settings'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='login'),
    #url(r'^logout/$', views.logout, name='logout'),
    url(r'^auth/', include('social_django.urls', namespace='social'))  # <- Here
]

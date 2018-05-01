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
    path('update_u/', views.update_user_settings, name = 'update_settings'),
    path('update_pic/', views.update_pic, name = 'update_pic'),
    url(r'^admin/', admin.site.urls),
    url(r'^profile/', views.view_profile),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.session_logout, name='logout'),
    url(r'^auth/', include('social_django.urls', namespace='social'))  # <- Here
]

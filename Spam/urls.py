from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.Index, name="home"),  # Maps the root URL to the index view
    path('index/', views.Index, name="Index"),
    path('about/', views.about, name="about"),
    path('contactus/', views.contactus, name="contactus"),
    path('check/', views.check_spam, name="CheckSpam"),
    path('upload', views.upload_file, name="upload"),
]
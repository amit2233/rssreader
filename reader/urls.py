from django.urls import path, include
from . import views


urlpatterns = [
    path('home', views.home),
    path('feeds', views.rss_feeds)
]
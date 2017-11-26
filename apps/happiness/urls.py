from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^main$', views.index),
    url(r'^travels$', views.travels),
    url(r'^add$', views.add),
    url(r'^logout$', views.logout),
    url(r'^home$', views.home),
    url(r'^destination/(?P<id>\d+)$', views.destination),
    url(r'^travels/add$', views.addtravels),
    url(r'^join/(?P<id>\d+)$', views.join)

]
from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index),
  url(r'^registration$', views.registration),
  url(r'^login$', views.login),
  url(r'^successlog$', views.successlog),
  url(r'^successreg$', views.successreg),
  url(r'^logout$', views.logout),
  url(r'^new$', views.new),
  url(r'^additem$', views.additem),
  url(r'^delete/(?P<id>\d+)$', views.delete),
  url(r'^bid/(?P<id>\d+)$', views.bid),
  url(r'^newbid/(?P<id>\d+)$', views.newbid),
  url(r'^home$', views.home),
]

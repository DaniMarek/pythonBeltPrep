from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index),
  url(r'^registration$', views.registration),
  url(r'^login$', views.login),
  url(r'^successlog$', views.successlog),
  url(r'^successreg$', views.successreg),
  url(r'^logout$', views.logout),
]

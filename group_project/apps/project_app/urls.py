from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^preferences$', views.preferences),
    url(r'^validate_register$', views.validate_register),
    url(r'^validate_login$', views.validate_login),
    url(r'^login_success$', views.success),
    url(r'^logout$', views.logout),
    url(r'^wheel$', views.wheel),
    url(r'^process_preferences$', views.process_preferences),
    url(r'^process_wheel$', views.process_wheel),
    url(r'^results$', views.results),
]
from django.conf.urls import url
from django.contrib import admin
from message import views

# template tagging for relative url
app_name = 'message'

urlpatterns = [
	url(r'^$', views.home, name='home'),
    url(r'^inbox$', views.inbox, name='inbox'),
    url(r'^outbox$', views.outbox, name='outbox'),
    url(r'^compose$', views.compose, name='compose'),
]


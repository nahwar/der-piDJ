from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<user_id>[1-9](?:\d+)?)/$', views.userindex, name='userindex'),
    url(r'^(?P<user_id>[1-9](?:\d+)?)/apikey/$', views.apikey, name='apikey'),
    url(r'^(?P<user_id>[1-9](?:\d+)?)/(?P<search_id>[1-9](?:\d+)?)/$', views.show, name='show'),
    url(r'^(?P<user_id>[1-9](?:\d+)?)/(?P<search_id>[1-9](?:\d+)?)/(?P<image_id>[1-9](?:\d+)?)/$', views.showimage, name='image'),
    url(r'^(?P<user_id>[1-9](?:\d+)?)/(?P<search_id>[1-9](?:\d+)?)/(?P<image_id>[1-9](?:\d+)?)/delete/$', views.deleteimage, name='deleteimage'),
    url(r'^(?P<user_id>[1-9](?:\d+)?)/(?P<search_id>[1-9](?:\d+)?)/update/$', views.update, name='update'),
    url(r'^(?P<user_id>[1-9](?:\d+)?)/(?P<search_id>[1-9](?:\d+)?)/delete/$', views.delete, name='delete'),
    url(r'^new/$', views.new, name='new'),
    url(r'^create/$', views.create, name='create'),
    url(r'^login', views.login, name='login'),
    url(r'^kollog', views.kollog, name='kollog'),
    url(r'^logout/$', views.logout_path, name='logout_path'),
]

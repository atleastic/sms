from myapp import views

__author__ = 'naman'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('myapp.views',
    url(r'^list/$',views.list, name='list'),
    url(r'^f_req/$',views.f_req,name='f_req'),
    url(r'^dp/$',views.dp,name='dp'),
)
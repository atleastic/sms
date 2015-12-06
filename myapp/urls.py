from myapp import views

__author__ = 'naman'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('myapp.views',
    url(r'^list/$',views.list, name='list'),
    url(r'^f_req/$',views.f_req,name='f_req'),
    url(r'^acc_req/$',views.acc_req,name='acc_req'),
    url(r'^get_status/$',views.get_status,name='get_status'),
    url(r'^dp/$',views.dp,name='dp'),
)
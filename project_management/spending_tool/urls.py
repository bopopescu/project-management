from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from spending_tool import views

urlpatterns = patterns('',

    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^financial_info/$', views.financial_info, name='financial_info'),
   # url(r'^add_field/$', views.add_field, name='add_field'),
    url(r'^add_current_field/$', views.add_current_field, name='add_current_field'),
    url(r'^review_info/$', views.review_info, name='review_info'),

    url(r'^report/$', views.report, name='report'),

  )
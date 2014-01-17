from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from spending_tool import views

urlpatterns = patterns('',

    url(r'^login/$', views.login, name='login'),
    url(r'^financial_info/$', views.financial_info, name='financial_info'),
    url(r'^add_field/$', views.add_field, name='add_field'),
    url(r'^review_info/$', views.review_info, name='review_info'),

  )
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from spending_tool import views

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='home/', permanent=False), name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^financial_info/$', views.financial_info, name='financial_info'),
   # url(r'^add_field/$', views.add_field, name='add_field'),
    url(r'^add_current_field/$', views.add_current_field, name='add_current_field'),
    url(r'^review_info/$', views.review_info, name='review_info'),
    url(r'^edit_status/$', views.edit_status, name='edit_status'),
  	url(r'^project_summary/$', views.project_summary, name='project_summary'),
  	url(r'^input_milestones/$', views.input_milestones, name='input_milestones'),
  	url(r'^project_details/$', views.project_details, name='project_details'),
    #url(r'^home/$', views.home, name='home'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^attach_document/$', views.attach_document, name='attach_document'),
    url(r'^home/$', views.home, name='home'),
    url(r'^guidelines/$', views.guidelines, name='guidelines'),
    #url(r'^download_document/$', views.download_document, name='download_document'),
   # url(r'^report/$', views.report, name='report'),

  

  )
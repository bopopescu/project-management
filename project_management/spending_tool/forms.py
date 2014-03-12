from spending_tool.models import *
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms

class StatusForm(ModelForm):
	class Meta:
		model = DescriptionType
		fields = ('recent_accomplishments', 'current_challenges', 'next_steps')
'''
class MilestoneForm(ModelForm):
	class Meta:
		model = DescriptionType
		fields = ('major_milestone', 'due_date', 'percentage_complete')
'''
class DetailsForm(ModelForm):
	class Meta:
		model = Project
		fields = ('start_date', 'funding_approved', 'engineering_mgr', 'target_completion', 'spent_cost',
		 'executive_sponsor', 'ip_generated', 'adoptor', 'committee')
			
class ProjectsummaryForm(ModelForm):
	class Meta:
		model = Project
		fields = ('project_overview', 'business_value_to_cisco')

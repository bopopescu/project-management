from spending_tool.models import *
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from spending_tool.models import *
from datefunction import return_quarter_year



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
	start_date = forms.DateField( widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
	target_completion = forms.DateField( widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
	class Meta:
		model = Project
		fields = ('start_date', 'engineering_mgr', 'target_completion',
		 'executive_sponsor', 'ip_generated', 'adoptor', 'committee')
			
class ProjectsummaryForm(ModelForm):
	class Meta:
		model = Project
		fields = ('project_overview', 'business_value_to_cisco')

class UploadFileForm(ModelForm):
    class Meta:
        model = Document
        fields =('file_name', 'document')

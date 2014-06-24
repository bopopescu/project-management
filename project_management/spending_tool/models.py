from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import *
# Create your models here.
import os
from project_management.settings import *
from datefunction import return_quarter_year

class UserProfile(models.Model):
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length = 20, null=True)

    class Meta:
        abstract=True


class EngineerProfile(UserProfile):
    user=models.OneToOneField(User, unique=True, related_name="engineer")
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.last_name) or u''

class Project(models.Model):
    STATUS=(
      ('Complete','Complete'),
      ('Ended','Ended'),
      ('Active','Active'),
      ('Need Review','Need Review'))
    status=models.CharField(max_length=100, choices=STATUS, default=None, null=True)
    name_project=models.CharField(max_length=100, null=True)
    project_overview = models.TextField(max_length=500, null=True, default=None)
    business_value_to_cisco = models.TextField(max_length=500, null=True, default=None)

    start_date = models.DateField( null=True)
    funding_approved = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    engineering_mgr = models.CharField(max_length=50, null=True, default=None)
    target_completion =models.DateField( null=True)
    #spent_qrt = models.CharField(max_length=1, null=True)
    spent_cost = models.DecimalField(max_digits=20, decimal_places=2, null=True, default=0) 
    executive_sponsor = models.CharField(max_length=50, null=True, default=None)
    ip_generated = models.CharField(max_length=100, null=True)
    adoptor = models.CharField(max_length=100, null=True, default=None)
    committee = models.CharField(max_length=100, null=True, default=None)


    modified_by = models.CharField(max_length=100, null=True, default=None)

    updated = models.DateTimeField(auto_now=True)   
    #fellow_engineer = models.ForeignKey(EngineerProfile)
    def __unicode__(self):
        return unicode(self.name_project) or u''
class Document(models.Model):
  document = models.FileField(upload_to=os.path.join(MEDIA_ROOT,'media/%Y/%m/%d'))
  date=models.DateField( null=True)
  project=models.ForeignKey(Project)
  file_name = models.CharField(max_length=50, null=True)

  

#class tmpProject(models.Model):
#    project_id = models.DecimalField(max_digits=3, decimal_places=0)
class projectTotalExpenses(models.Model):
    project=models.ForeignKey(Project)
    actual_spent=models.DecimalField(max_digits=10, decimal_places=0, default=0)
    funding_approved=models.DecimalField(max_digits=10, decimal_places=0, default=0)

class ExpensesType(models.Model):
    expenses_type=models.CharField(max_length=100, null=True)
    estimated_cost = models.DecimalField(max_digits=5, decimal_places=0)
    
    relates_to=models.ForeignKey('self', null=True, default=None)
    project=models.ForeignKey(Project)
    year = models.DecimalField(max_digits=4, decimal_places=0)
    cross_charge_actual_cost=models.DecimalField(max_digits=5, decimal_places=1)
    direct_charge_actual_cost = models.DecimalField(max_digits=5, decimal_places=1)
    #department_number=models.CharField(max_length=100, null=True, default=None)

    quarter_number=models.DecimalField(max_digits=1, decimal_places=0)
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.expenses_type) or u''
        
class DepartmentNumber(models.Model):
    department_number=models.CharField(max_length=100, null=True, default=None)
    cross_charge_actual_cost=models.DecimalField(max_digits=5, decimal_places=1)
    relates_to=models.ForeignKey(ExpensesType)
    person=models.CharField(max_length=100, null=True, default=None)
    
class DescriptionType(models.Model):
    recent_accomplishments = models.TextField(max_length=500, null=True, default=None)
    current_challenges = models.TextField(max_length=500, null=True, default=None)
    next_steps = models.TextField(max_length=500, null=True, default=None)
    quarter_number=models.DecimalField(max_digits=1, decimal_places=0)
    year = models.DecimalField(max_digits=4, decimal_places=0)
    date=models.DateField( null=True)
    project = models.ForeignKey(Project)
 
class Milestone(models.Model):
    major_milestone = models.CharField(max_length=100, null=True)  
    due_date = models.DateField( null=True)
    percentage_complete = models.DecimalField(max_digits=3, decimal_places=0)
    quarter_number=models.DecimalField(max_digits=1, decimal_places=0)
    year = models.DecimalField(max_digits=4, decimal_places=0)
    date=models.DateField( null=True)
    project = models.ForeignKey(Project)


class Report(models.Model):
    datetime_created=models.DateTimeField(null=True)
    file_name=models.FileField(upload_to='media/%Y/%m/%d')
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.datetime_created) or u''

def create_default_expenses(sender, instance, created, **kwargs):
    if created:
      today=datetime.today()
      date=return_quarter_year()
      types=['Other','Travel','Intern' ,'Contractor','FTE','Capital Equipment','Equipment']
      for t in types:
          ExpensesType.objects.create(
          expenses_type= t,
          year=date[1],
          quarter_number=date[0],
          direct_charge_actual_cost=0,
          cross_charge_actual_cost=0,
          estimated_cost=0,
          project=instance
          )
      DescriptionType.objects.create(project=instance,
                                    quarter_number=date[0],
                                    year=date[1],
                                    date=today,
                                     )

def create_total_exp(sender, instance, created, **kwargs):
    if created:
        projectTotalExpenses.objects.create(project=instance)




post_save.connect(create_default_expenses, sender=Project)

post_save.connect(create_total_exp, sender=Project)
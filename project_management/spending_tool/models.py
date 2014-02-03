from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import *
# Create your models here.

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
      ('Need Review','Need Review'))
    status=models.CharField(max_length=100, choices=STATUS, default=None, null=True)
    name_project=models.CharField(max_length=100, null=True)
    project_overview = models.TextField(max_length=500, null=True)
    business_value_to_cisco = models.TextField(max_length=500, null=True)
    fellow_engineer = models.ForeignKey(EngineerProfile)
    def __unicode__(self):
        return unicode(self.name_project) or u''

class ExpensesType(models.Model):
    expenses_type=models.CharField(max_length=100, null=True)
    estimated_cost = models.DecimalField(max_digits=5, decimal_places=0)
    
    relates_to=models.ForeignKey('self', null=True, default=None)
    project=models.ForeignKey(Project)
    year = models.DecimalField(max_digits=4, decimal_places=0)
    cross_charge_actual_cost=models.DecimalField(max_digits=5, decimal_places=0)
    direct_charge_actual_cost = models.DecimalField(max_digits=5, decimal_places=0)
    department_number=models.CharField(max_length=100, null=True, default=None)

    quarter_number=models.DecimalField(max_digits=1, decimal_places=0)
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.expenses_type) or u''

class DescriptionType(models.Model):
    recent_accomplishments = models.TextField(max_length=500, null=True)
    current_challenges = models.TextField(max_length=500, null=True)
    next_steps = models.TextField(max_length=500, null=True)
    major_milestone = models.TextField(max_length=100, null=True)
    due_date = models.CharField(max_length=11, null=True)
    percentage_complete = models.DecimalField(max_digits=3, decimal_places=0)
    project = models.ForeignKey(Project)


def create_default_expenses(sender, instance, created, **kwargs):
    if created:
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


def return_quarter_year():
  time=datetime.now()
  year=time.year
  month=time.month
  day=time.day    
  if month==7 and day>=27:
      quarter_number==1
      year=year+1
  if month==8 or month==9:
      quarter_number=1
      year=year+1
  if month == 10 and day <27:
      quarter_number=1
      year=year+1
  if month==10 and day >= 26:
      quarter_number=2
      year=year+1
  if month==11 or month == 12:
      quarter_number=2
      year=year+1
  if month==1 and day <26:
      quarter_number=2
  if month==1 and day >=26:
      quarter_number=3
  if month==2 or month==3:
      quarter_number=3
  if month==4 and day<27:
      quarter_number=3
  if month==4 and day >=27:
      quarter_number=4
  if month==5 or month==6:
      quarter_number=4
  if month==7 and day<27:
      quarter_number=4
  date=[quarter_number, year]
  return date



post_save.connect(create_default_expenses, sender=Project)


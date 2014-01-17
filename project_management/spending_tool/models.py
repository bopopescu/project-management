from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length = 20, null=True)
    business_unit=models.ForeignKey(BusinessUnit)

    class Meta:
    	abstract=True


class EngineerProfile(UserProfile):
    user=models.OneToOneField(User, unique=True, related_name="engineer")



class Project(models.Model):
	name_project=models.CharField(max_length=100, null=True)
	description = TextField(max_length=200, null=True)
	fellow_engineer = models.ForeignKey(EngineerProfile)

class Quarter(models.Model):

	project=models.ForeignKey(Project)

	QUARTER_NUMBER=(
      ('4','4'),
      ('3','3'),
      ('2','2'),
      ('1','1'),

    )
    quarter_number=models.CharField(max_length=1,
                                       choices=QUARTER_NUMBER,
                                       default='None', null=True)
    year=models.DecimalField(max_digits=2)

class ExpensesType(models.Model):
	name=models.CharField(max_length=100, null=True)
	estimated_cost = models.DecimalField(max_digits=5, decimal_places=2)
	actual_cost = models.DecimalField(max_digits=5, decimal_places=2)
	quarter=models.ForeignKey(Quarter)






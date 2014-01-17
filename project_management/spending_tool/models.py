from django.db import models
from django.contrib.auth.models import User
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
    name_project=models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=200, null=True)
    fellow_engineer = models.ForeignKey(EngineerProfile)
    def __unicode__(self):
        return unicode(self.name_project) or u''



class ExpensesType(models.Model):
    expenses_type=models.CharField(max_length=100, null=True)
    estimated_cost = models.DecimalField(max_digits=5, decimal_places=0)
    actual_cost = models.DecimalField(max_digits=5, decimal_places=0)
    relates_to=models.ForeignKey('self', null=True, default=None)
    project=models.ForeignKey(Project)
    year = models.DecimalField(max_digits=4, decimal_places=0)

    quarter_number=models.DecimalField(max_digits=1, decimal_places=0)
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.expenses_type) or u''








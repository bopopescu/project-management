from django.contrib import admin
from spending_tool.models import *
from django.contrib.auth.models import User



class EngineerAdmin(admin.ModelAdmin):
	model=EngineerProfile

	fieldsets=[
       ('Info',{'fields':['user','first_name','last_name']}),
	]

	def first_name(self, instance):
		return instance.user.first_name
	def last_name(self, instance):
		return instance.user.last_name


admin.site.register(EngineerProfile, EngineerAdmin)

class ProjectAdmin(admin.ModelAdmin):
	model=Project

	fieldsets=[
	('Info',{'fields':['status' ,'name_project','fellow_engineer','description']})
	]
admin.site.register(Project, ProjectAdmin)

class ExpensesTypeAdmin(admin.ModelAdmin):
	model=ExpensesType

	fieldsets=[
	('Info',{'fields':['expenses_type', 'year', 'quarter_number','estimated_cost','direct_charge_actual_cost',
		'cross_charge_actual_cost','department_number' ,'project']})
	]
admin.site.register(ExpensesType, ExpensesTypeAdmin)

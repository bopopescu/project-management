from django.contrib import admin
from spending_tool.models import *
from django.contrib.auth.models import User
from datetime import *
import xlsxwriter 
from django.http import HttpResponse
'''
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
'''
class ProjectAdmin(admin.ModelAdmin):
	model=Project

	fieldsets=[

	('Info',{'fields':['status' ,'name_project','project_overview','business_value_to_cisco','start_date',
	 'funding_approved', 'engineering_mgr', 'target_completion', 'spent_cost', 'executive_sponsor',
	 'ip_generated', 'adoptor', 'committee']}),

	]
	readonly_fields=['project_overview','business_value_to_cisco','start_date', 'engineering_mgr',
	 'target_completion',  'executive_sponsor',
	 'ip_generated', 'adoptor', 'committee']
	actions=['print_report']

	def print_report(modeladmin, request, queryset):
		try:
			import cStringIO as StringIO
		except ImportError:
			import StringIO
		time=datetime.now()
		year=time.year
		day=time.day
		month=time.month
		hour=time.hour
		minute=time.minute
		output = StringIO.StringIO()
		title=str('report_date_%d_%d_%d_time_%d_%d.xlsx' %(month, day, year, hour, minute))
		#workbook=xlsxwriter.Workbook('report_%s.xlsx' %(queryset.test))	
		workbook=xlsxwriter.Workbook(output)
		#workbook=xlsxwriter.Workbook('blablabla.xlsx')
		worksheet = workbook.add_worksheet()
		line=1
		
		list_quarters=[]
		#project_id=queryset.id
		for query in queryset:
			cell=0
			for m in range(4):
				if len(ExpensesType.objects.filter(project=query, year=year, quarter_number=m+1))>0:
					list_quarters.append(ExpensesType.objects.filter(project=query, year=year, quarter_number=m+1))
			for p in range(len(list_quarters)):
				worksheet.write(line-1, 1+cell, 'Year'+str(list_quarters[p][0].year))
				worksheet.write(line-1, 2+cell, 'Quarter'+str(list_quarters[p][0].quarter_number))
				worksheet.write(line, 1+cell, 'Expense Type' )
				worksheet.write(line, 2+cell, 'Estimates' )
				worksheet.write(line, 3+cell, 'Direct Charge' )
				worksheet.write(line, 4+cell, 'Cross Charge' )
				num_of_expenses_per_quarter=len(list_quarters[p])
				direct_expenses_per_quarter=0
				cross_expenses_per_quarter=0
				for n in range(len(list_quarters[p])):
					worksheet.write(n+line+1, 1+cell, list_quarters[p][n].expenses_type)
					worksheet.write(n+line+1, 2+cell, list_quarters[p][n].estimated_cost)
					worksheet.write(n+line+1, 3+cell, list_quarters[p][n].direct_charge_actual_cost)
					worksheet.write(n+line+1, 4+cell, list_quarters[p][n].cross_charge_actual_cost)
					direct_expenses_per_quarter=direct_expenses_per_quarter+list_quarters[p][n].direct_charge_actual_cost
					cross_expenses_per_quarter=cross_expenses_per_quarter+list_quarters[p][n].cross_charge_actual_cost

                
				worksheet.write(num_of_expenses_per_quarter+line+1, 3+cell,'Total: '+ str(direct_expenses_per_quarter))
				worksheet.write(num_of_expenses_per_quarter+line+1, 4+cell,'Total: '+ str( cross_expenses_per_quarter))
				#get departments
				list_dept=[]
				worksheet.write(line+num_of_expenses_per_quarter+3, 1+cell, 'Cross Charges')
				worksheet.write(line+num_of_expenses_per_quarter+4, 1+cell, 'Expense Type')
				worksheet.write(line+num_of_expenses_per_quarter+4, 2+cell, 'Cross Charge')
				worksheet.write(line+num_of_expenses_per_quarter+4, 3+cell, 'Dept #')
				tmp=0
				for dept in list_quarters[p]:
					departments=DepartmentNumber.objects.filter(relates_to=dept)
					for department in departments:
						worksheet.write(line+num_of_expenses_per_quarter+5+tmp, 1+cell, dept.expenses_type)
						worksheet.write(line+num_of_expenses_per_quarter+5+tmp, 2+cell, department.cross_charge_actual_cost)
						worksheet.write(line+num_of_expenses_per_quarter+5+tmp, 3+cell, department.department_number)
						tmp=tmp+1
				cell=cell+5
			line=line+20
		workbook.close()
		output.seek(0)
		response = HttpResponse(output.read(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
		response['Content-Disposition'] = "attachment; filename="+title
		return response

	print_report.short_description = "Export to Excel"

admin.site.register(Project, ProjectAdmin)

class ReportAdmin(admin.ModelAdmin):
	model=Report
	fieldsets=[('Info',{'fields':['datetime_created','file_name']})]
admin.site.register(Report, ReportAdmin)


class ExpensesTypeAdmin(admin.ModelAdmin):
	model=ExpensesType

	fieldsets=[
	('Info',{'fields':['expenses_type', 'year', 'quarter_number','estimated_cost','direct_charge_actual_cost',
		'cross_charge_actual_cost' ,'project']})
	]
admin.site.register(ExpensesType, ExpensesTypeAdmin)

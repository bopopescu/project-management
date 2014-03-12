from django.contrib import admin
from spending_tool.models import *
from django.contrib.auth.models import User
from datetime import *
import xlsxwriter 
from django.http import HttpResponse

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

	('Info',{'fields':['status' ,'name_project','fellow_engineer','project_overview','business_value_to_cisco','start_date',
	 'funding_approved', 'engineering_mgr', 'target_completion', 'spent_cost', 'executive_sponsor',
	 'ip_generated', 'adoptor', 'committee']}),

	]
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
		line=0
		
		list_quarters=[]
		#project_id=queryset.id
		for query in queryset:
			cell=0
			for m in range(4):
				if len(ExpensesType.objects.filter(project=query, year=year, quarter_number=m+1))>0:
					list_quarters.append(ExpensesType.objects.filter(project=query, year=year, quarter_number=m+1))
			for p in range(len(list_quarters)):
				worksheet.write(line, 1+cell, 'Expense Type' )
				worksheet.write(line, 2+cell, 'Estimates' )
				worksheet.write(line, 3+cell, 'Direct Charge' )
				worksheet.write(line, 4+cell, 'Cross Charge' )
				for n in range(len(list_quarters[p])):
					worksheet.write(n+line+1, 1+cell, list_quarters[p][n].expenses_type)
					worksheet.write(n+line+1, 2+cell, list_quarters[p][n].estimated_cost)
					worksheet.write(n+line+1, 3+cell, list_quarters[p][n].direct_charge_actual_cost)
					worksheet.write(n+line+1, 4+cell, list_quarters[p][n].quarter_number)
				cell=cell+5
			line=line+20
		workbook.close()
		output.seek(0)
		response = HttpResponse(output.read(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
		response['Content-Disposition'] = "attachment; filename="+title
		return response

	print_report.short_description = "Print report"

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
'''
class DescriptionTypeAdmin(admin.ModelAdmin):
	model = DescriptionType

	fieldsets = [
	('Status',{'fields':['project','recent_accomplishments','current_challenges','next_steps',
		'major_milestone','due_date','percentage_complete',]}),
	]
admin.site.register(DescriptionType, DescriptionTypeAdmin)

def print_report(modeladmin, request, queryset):
    time=datetime.now()
    year=time.year
    day=time.day
    month=time.month
    workbook=xlsxwriter.Workbook('report.xlsx')    
    worksheet = workbook.add_worksheet()
    line=0

    #project_id=queryset.id
	for m in range(4):
		if len(ExpensesType.objects.filter(project=query, year=year, quarter_number=m+1))>0:
			list_quarters.append(ExpensesType.objects.filter(project=projects[i], year=year, quarter_number=m+1))
		cell=0
    for p in range(len(list_quarters)):
        worksheet.write(line, 1+cell, 'Expense Type' )
        worksheet.write(line, 2+cell, 'Estimates' )
        worksheet.write(line, 3+cell, 'Direct Charge' )
        worksheet.write(line, 4+cell, 'Cross Charge' )
        for n in range(len(list_quarters[p])):
            worksheet.write(n+line+1, 1+cell, list_quarters[p][n].expenses_type)
            worksheet.write(n+line+1, 2+cell, list_quarters[p][n].estimated_cost)
            worksheet.write(n+line+1, 3+cell, list_quarters[p][n].direct_charge_actual_cost)
            worksheet.write(n+line+1, 4+cell, list_quarters[p][n].quarter_number)
        cell=cell+5
    workbook.close()
print_report.short_description = "Print report"
def print_report_all(modeladmin, request, queryset):
    time=datetime.now()
    year=time.year
    day=time.day
    month=time.month
    workbook=xlsxwriter.Workbook('report.xlsx')
    #workbook = xlsxwriter.Workbook('tech_fund_report_'+ str(month) +'/'+ str(day) +'/' + str(year) +'.xlsx')
    worksheet = workbook.add_worksheet()



    projects=Project.objects.all() 
    line=0
    list_quarters=[]
    for i in range(len(projects)):
        for m in range(4):
            if len(ExpensesType.objects.filter(project=projects[i], year=year, quarter_number=m+1))>0:
                list_quarters.append(ExpensesType.objects.filter(project=projects[i], year=year, quarter_number=m+1))
        cell=0
        for p in range(len(list_quarters)):
            worksheet.write(line, 1+cell, 'Expense Type' )
            worksheet.write(line, 2+cell, 'Estimates' )
            worksheet.write(line, 3+cell, 'Direct Charge' )
            worksheet.write(line, 4+cell, 'Cross Charge' )
            for n in range(len(list_quarters[p])):
                worksheet.write(n+line+1, 1+cell, list_quarters[p][n].expenses_type)
                worksheet.write(n+line+1, 2+cell, list_quarters[p][n].estimated_cost)
                worksheet.write(n+line+1, 3+cell, list_quarters[p][n].direct_charge_actual_cost)
                worksheet.write(n+line+1, 4+cell, list_quarters[p][n].quarter_number)
            cell=cell+5
        line=line+20
    workbook.close()
'''
from spending_tool.models import *
from datetime import *
import xlsxwriter 
from django.http import HttpResponse

def createReport(*args):
    time=datetime.now()
    year=time.year
    day=time.day
    month=time.month
    hour=time.hour
    minute=time.minute
    projects=[]
    try:
        if len(args[0])>0:
            projects=args[0]
            title=str('report_date_%d_%d_%d_time_%d_%d.xlsx' %(month, day, year, hour, minute))
    except TypeError:
        projects=[args[0]]
        title=str(projects[0].name_project)
    try:
        import cStringIO as StringIO
    except ImportError:
        import StringIO
    output = StringIO.StringIO() 
    #workbook=xlsxwriter.Workbook('report_%s.xlsx' %(queryset.test))    
    workbook=xlsxwriter.Workbook(output)
    #workbook=xlsxwriter.Workbook('blablabla.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    year=time.year
    for project in projects:
        line=2
        cell=0
        list_quarters=[]
        worksheet.write(line-2, 1, 'Project', bold)
        worksheet.write(line-2, 2, str(project.name_project))
        worksheet.write(line-2, 3, 'Last Updated', bold)
        worksheet.write(line-2, 4, str(project.updated.month)+'/'+ str(project.updated.day)+'/'+str(project.updated.year))
        for m in range(4):
            if len(ExpensesType.objects.filter(project=project, year=year, quarter_number=m+1))>0:
                list_quarters.append(ExpensesType.objects.filter(project=project, year=year, quarter_number=m+1))
        for p in range(len(list_quarters)):
            worksheet.write(line-1, 1+cell, 'Year'+str(list_quarters[p][0].year), bold)
            worksheet.write(line-1, 2+cell, 'Quarter'+str(list_quarters[p][0].quarter_number), bold)
            worksheet.write(line, 1+cell, 'Expense Type', bold )
            worksheet.write(line, 2+cell, 'Estimates', bold  )
            worksheet.write(line, 3+cell, 'Direct Charge', bold  )
            worksheet.write(line, 4+cell, 'Cross Charge', bold  )
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

            
            worksheet.write(num_of_expenses_per_quarter+line+1, 3+cell,'Total: '+ str(direct_expenses_per_quarter), bold )
            worksheet.write(num_of_expenses_per_quarter+line+1, 4+cell,'Total: '+ str( cross_expenses_per_quarter), bold )
            #get departments
            list_dept=[]
            worksheet.write(line+num_of_expenses_per_quarter+3, 1+cell, 'Cross Charges', bold )
            worksheet.write(line+num_of_expenses_per_quarter+4, 1+cell, 'Expense Type', bold )
            worksheet.write(line+num_of_expenses_per_quarter+4, 2+cell, 'Cross Charge', bold )
            worksheet.write(line+num_of_expenses_per_quarter+4, 3+cell, 'Dept #', bold )
            tmp=0
            for dept in list_quarters[p]:
                departments=DepartmentNumber.objects.filter(relates_to=dept)
                for department in departments:
                    worksheet.write(line+num_of_expenses_per_quarter+5+tmp, 1+cell, dept.expenses_type)
                    worksheet.write(line+num_of_expenses_per_quarter+5+tmp, 2+cell, department.cross_charge_actual_cost)
                    worksheet.write(line+num_of_expenses_per_quarter+5+tmp, 3+cell, department.department_number)
                    tmp=tmp+1
            cell=cell+5
    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+title
    print '##############################'+title
    return response
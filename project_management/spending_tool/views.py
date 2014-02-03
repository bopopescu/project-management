# Create your views here.
import os
import xlsxwriter  
import csv
import time, threading
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from spending_tool.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as django_logout
from django.template import RequestContext
from datetime import *

def login(request):
    username=password=''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username =username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/financial_info/')
            else:
                return HttpResponseRedirect('/login/')
        else:
            return HttpResponseRedirect('spending_tool/login/')
    return render(request, 'spending_tool/login.html', {'username':username, 'password':password})

def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/login/')


def financial_info(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
    	current_user=request.user
        engineer=EngineerProfile.objects.get(user=current_user)
        project=Project.objects.get(fellow_engineer=engineer)
        
        date = return_quarter_year()
        quarter_number=date[0]
        year=date[1]
        expenses_for_next_quarter=[]
        expenses_for_current_quarter=ExpensesType.objects.filter(
        														year=year,
        														quarter_number=quarter_number,
        														project=project)
        
        if quarter_number ==2 or quarter_number==3:
            expenses_for_previous_quarter=ExpensesType.objects.filter(
        															year=year,
        															quarter_number=quarter_number-1,
        															project=project)
            #expenses_for_next_quarter= expenses_for_next_quarter.append(ExpensesType.objects.filter(
            #														year=year,
            #														quarter_number=quarter_number+1,
            #														project=project) )
        if quarter_number==1:
        	expenses_for_previous_quarter=ExpensesType.objects.filter(
        															year=year-1,
        															quarter_number=4,
        															project=project)
        	#expenses_for_next_quarter.append(ExpensesType.objects.filter(
            #														year=year,
            #														quarter_number=2,
            #														project=project) )
        if quarter_number==4:
            expenses_for_previous_quarter=ExpensesType.objects.filter(
        															year=year,
        															quarter_number=quarter_number-1,
        															project=project)
            #expenses_for_next_quarter.append(ExpensesType.objects.filter(
            #														year=year+1,
            #														quarter_number=1,
            #														project=project) )
            
        for expense in expenses_for_current_quarter:
        	if len(ExpensesType.objects.filter(relates_to=expense)) == 0:
        		if quarter_number ==1 or quarter_number==2 or quarter_number==3:
        			expenses_for_next_quarter.append( ExpensesType.objects.create( project=project,
        										relates_to=expense,
        										year=year,
        										quarter_number=quarter_number+1,
        										expenses_type=expense.expenses_type,
        										estimated_cost=0,
        										cross_charge_actual_cost=0,
        										direct_charge_actual_cost=0) )
        		if quarter_number == 4:
        			expenses_for_next_quarter.append( ExpensesType.objects.create( project=project,
        										relates_to=expense,
        										year=year+1,
        										quarter_number=1,
        										expenses_type=expense.expenses_type,
        										estimated_cost=0,
        										cross_charge_actual_cost=0,
        										direct_charge_actual_cost=0) )
        	else:
        	    #if not ExpensesType.objects.get(relates_to=expense) in expenses_for_next_quarter:
        	    expenses_for_next_quarter.append(ExpensesType.objects.get(relates_to=expense))

        if request.method=='POST':
            i=0
            expected_cost=request.POST.getlist('expected_cost')
            actual_cost=request.POST.getlist('actual_cost')
            for expense in expenses_for_current_quarter:
            	expense.actual_cost=actual_cost[i]
            	expense.save()
            	expense_for_next_quarter=ExpensesType.objects.get(relates_to=expense)
                expense_for_next_quarter.estimated_cost=expected_cost[i]
                expense_for_next_quarter.save()
            	i=i+1
            return HttpResponseRedirect('/review_info/')
    return render(request,'spending_tool/financial_info.html',{ 'expenses_for_next_quarter':expenses_for_next_quarter,
    															'expenses_for_current_quarter':expenses_for_current_quarter,
    															'expenses_for_previous_quarter':expenses_for_previous_quarter,
    															'project':project,
    															'quarter_number':quarter_number
    															})



'''

def financial_info(request):
    i=0
    expenses_for_next_quarter=current_expenses=''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        current_user=request.user
        engineer=EngineerProfile.objects.get(user=current_user)
        project=Project.objects.get(fellow_engineer=engineer)
        
        date = return_quarter_year()
        quarter_number=date[0]
        year=date[1]	
        previous_expensestype=[]
        expense_for_current_quarter=ExpensesType.objects.filter(
        														year=year,
        														quarter_number=quarter_number,
        														project=project)

        
        if request.method == 'POST':
            if quarter_number== 1:
                
                for current_expenses in expense_for_current_quarter:
                    name= current_expenses.expenses_type
                    expected_cost=request.POST.getlist('expected_cost')
                    actual_cost=request.POST.getlist('actual_cost')
                    if len(ExpensesType.objects.filter(relates_to=current_expenses)) == 0:
                        expense_for_next_quarter=ExpensesType.objects.create(year=year,
                    							relates_to=current_expenses,
        										expenses_type=name, 
        										actual_cost=0,
        										estimated_cost=expected_cost[i],
        										project=project,
        										quarter_number=quarter_number+1,
        										)
                    else:
                    	expense_for_next_quarter=ExpensesType.objects.get(relates_to=current_expenses)
                    	expense_for_next_quarter.estimated_cost=expected_cost[i]
                    	expense_for_next_quarter.save()
                    current_expenses.actual_cost=actual_cost[i]
                    current_expenses.save()
                    expenses_for_next_quarter=ExpensesType.objects.filter(project=project,
                    													year=year,
                    													quarter_number=2)
                    previous_expensestype = ExpensesType.objects.filter(project=project, 
        														quarter_number=4,
        														year=year-1,
                    												)
                    i=i+1
                return HttpResponseRedirect('/review_info/')
            if quarter_number== 2 or quarter_number == 3:
                for current_expenses in expense_for_current_quarter:
                    name= current_expenses.expenses_type
                    expected_cost=request.POST.getlist('expected_cost')

                    actual_cost=request.POST.getlist('actual_cost')
                    
                    if len(ExpensesType.objects.filter(relates_to=current_expenses)) == 0:
                        expense_for_next_quarter=ExpensesType.objects.create(year=year,
                    							relates_to=current_expenses,
        										expenses_type=name, 
        										actual_cost=0,
        										estimated_cost=expected_cost[i],
        										project=project,
        										quarter_number=quarter_number+1,
        										)
                    else:
                    	expense_for_next_quarter=ExpensesType.objects.get(relates_to=current_expenses)
                    	expense_for_next_quarter.estimated_cost=expected_cost[i]
                    	expense_for_next_quarter.save()
                    current_expenses.actual_cost=actual_cost[i]
                    current_expenses.save()
                    expenses_for_next_quarter=ExpensesType.objects.filter(project=project,
                    													year=year,
                    													quarter_number=quarter_number+1)
                 
                    previous_expensestype = ExpensesType.objects.filter(project=project, 
        														quarter_number= quarter_number-1,
        														year=year,
        														)
                    i=i+1
                return HttpResponseRedirect('/review_info/')
            if quarter_number== 4:
                for current_expenses in expense_for_current_quarter:
                    name= current_expenses.expenses_type
                    expected_cost=request.POST.getlist('expected_cost')

                    actual_cost=request.POST.getlist('actual_cost')
                    
                    if len(ExpensesType.objects.filter(relates_to=current_expenses)) == 0:
                        expense_for_next_quarter=ExpensesType.objects.create(year=year+1,
                    							relates_to=current_expenses,
        										expenses_type=name, 
        										actual_cost=0,
        										estimated_cost=expected_cost[i],
        										project=project,
        										quarter_number=1,
        										)
                    else:
                    	expense_for_next_quarter=ExpensesType.objects.get(relates_to=current_expenses)
                    	expense_for_next_quarter.estimated_cost=expected_cost[i]
                    	expense_for_next_quarter.save()
                    current_expenses.actual_cost=actual_cost[i]
                    current_expenses.save()
                    expenses_for_next_quarter=ExpensesType.objects.filter(project=project,
                    													year=year+1,
                    													quarter_number=1)
                    
                    i=i+1
                return HttpResponseRedirect('/review_info/')
    return render(request,'spending_tool/financial_info.html',{ 'expenses_for_next_quarter':expenses_for_next_quarter,
    															'expense_for_current_quarter':expense_for_current_quarter,
    															'previous_expensestype':previous_expensestype,
    															'project':project,
    															'quarter_number':quarter_number
    															})    
        	

 '''   
'''

def add_field(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        current_user=request.user

        engineer=EngineerProfile.objects.get(user=current_user)
        project=Project.objects.get(fellow_engineer=engineer)
        
        date=return_quarter_year()
        quarter_number=date[0]
        year=date[1]



        expense_for_current_quarter=[]

        if request.method == 'POST':
            name = request.POST['name']
            expected_cost=request.POST['expected_cost']
            if quarter_number==1 or quarter_number==2 or quarter_number==3:          
                ExpensesType.objects.create(year=year,
        										expenses_type=name, 
        										actual_cost=0,
        										estimated_cost=expected_cost,
        										project=project,
        										quarter_number=quarter_number+1
        										)

            if quarter_number==4:
                ExpensesType.objects.create(year=year+1,
        										expenses_type=name, 
        										actual_cost=0,
        										estimated_cost=expected_cost,
        										project=project,
        										quarter_number=1
        										)
            return HttpResponseRedirect('/financial_info/')
            
        if quarter_number==1 or quarter_number==2 or quarter_number==3:
            expense_for_current_quarter=ExpensesType.objects.filter(
        														year=year,
        														quarter_number=quarter_number+1,
        														project=project)
        if quarter_number==4:
            expense_for_current_quarter=ExpensesType.objects.filter(
        														year=year+1,
        														quarter_number=1,
        														project=project)
		
    return render(request,'spending_tool/add_field.html',{'quarter_number':quarter_number, 'project':project, 'expense_for_current_quarter':expense_for_current_quarter})
'''
def add_current_field(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        current_user=request.user

        engineer=EngineerProfile.objects.get(user=current_user)
        project=Project.objects.get(fellow_engineer=engineer)
        
        date=return_quarter_year()
        quarter_number=date[0]
        year=date[1]
        if request.method=='POST':
            name = request.POST['name']
            department_number=request.POST.get('department_number','')
            cross_charge_actual_cost=request.POST.get('cross_charge_actual_cost','')
            direct_charge_actual_cost=request.POST.get('direct_charge_actual_cost','')
            expected_cost=request.POST['expected_cost']
            current=ExpensesType.objects.create(project=project,
            							expenses_type=name,
            							estimated_cost=expected_cost,
            							cross_charge_actual_cost=cross_charge_actual_cost,
            							direct_charge_actual_cost=direct_charge_actual_cost,
            							year=year,
            							quarter_number=quarter_number,
            							department_number=department_number)
            '''
            if quarter_number == 1 or quarter_number == 2 or quarter_number == 3:
            	ExpensesType.objects.create(project=project,
            							expenses_type=name,
            							estimated_cost=expected_cost,
            							actual_cost=actual_cost,
            							year=year,
            							quarter_number=quarter_number+1,
            							relates_to=current)
            if quarter_number==4:
            	ExpensesType.objects.create(project=project,
            							expenses_type=name,
            							estimated_cost=expected_cost,
            							actual_cost=actual_cost,
            							year=year+1,
            							quarter_number=1,
            							relates_to=current)
			'''
            return HttpResponseRedirect('/financial_info/')
    return render(request,'spending_tool/add_current_field.html',{'quarter_number':quarter_number, 'project':project})



def review_info(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
    	current_user=request.user
        engineer=EngineerProfile.objects.get(user=current_user)
        project=Project.objects.get(fellow_engineer=engineer)
        date=return_quarter_year()
        quarter_number=date[0]
        year=date[1]
        if quarter_number==1:
            previous_quarter=ExpensesType.objects.filter(project=project, year=year-1, quarter_number=4)
        if quarter_number==2:
            previous_quarter=ExpensesType.objects.filter(project=project, year=year, quarter_number=1)
        if quarter_number==3:
            previous_quarter=ExpensesType.objects.filter(project=project, year=year, quarter_number=2)
        if quarter_number==4:
            previous_quarter=ExpensesType.objects.filter(project=project, year=year, quarter_number=3)
        current_quarter = ExpensesType.objects.filter(project=project, year=year, quarter_number=quarter_number)
        if quarter_number== 1 or quarter_number==2 or quarter_number == 3:
            next_quarter=ExpensesType.objects.filter(project=project, year=year, quarter_number= quarter_number+1)
        if quarter_number== 4:
            next_quarter=ExpensesType.objects.filter(project=project, year=year+1, quarter_number= 1)


    return render(request,'spending_tool/review_info.html',{'project':project,
    														'quarter_number':quarter_number,
    														'previous_quarter':previous_quarter,
    													 	'current_quarter':current_quarter,
    													 	'next_quarter':next_quarter})





def print_report():
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

def send_email_before_end():
    time=datetime.now()
    year=time.year
    month=time.month
    day=time.day
    if month==10 and day<27 and day>20:
        send_mail()
    if month==1 and day<26 and day>19:
        send_mail()
    if month==4 and day<27 and day>20:
    	send_mail()
    if month==7 and day<27 and day>20:
    	send_mail()
    threading.Timer(172800, send_email_before_end).start()

def send_mail():
    subject='ACTION REQUIRED: Please fill Tech Fund fields'
    message='Please complete the spending review for your project on Tech Fund'
    from_email='ciip.team.1@gmail.com'
    email_engineers = EngineerProfile.objects.all()
    to_email=[]
    for email in email_engineers:
        to_email.append(email.user.email)
    try:
        send_mail(subject, message, from_email , to_email)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')	

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

def status(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        current_user = request.user
        engineer = EngineerProfile.objects.get(user=current_user)
        project = Project.objects.get(fellow_engineer=engineer)
        description = DescriptionType.objects.get(project=project)  
        recent_accomplishments = description.recent_accomplishments
        current_challenges = description.current_challenges
        next_steps = description.next_steps
              
    return render(request, 'spending_tool/status.html',{'project':project, 'recent_accomplishments':recent_accomplishments,
                                                    'current_challenges':current_challenges,
                                                    'next_steps':next_steps})

def project_summary(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        current_user = request.user
        engineer = EngineerProfile.objects.get(user=current_user)
        project = Project.objects.get(fellow_engineer=engineer)
        project_overview = project.project_overview
        business_value_to_cisco = project.business_value_to_cisco
    return render(request, 'spending_tool/project_summary.html',{'project':project,
                'project_overview':project_overview,
                'business_value_to_cisco':business_value_to_cisco})


def milestones(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        current_user = request.user
        engineer = EngineerProfile.objects.get(user=current_user)
        project = Project.objects.get(fellow_engineer=engineer)
        description = DescriptionType.objects.get(project=project)  
        major_milestone = description.major_milestone
        due_date = description.due_date
        percentage_complete = description.percentage_complete
    return render(request, 'spending_tool/milestones.html',{'project':project,
                                'major_milestone':major_milestone, 'due_date':due_date,
                                'percentage_complete':percentage_complete})

def project_details(request):
    return render(request, 'spending_tool/project_details.html')





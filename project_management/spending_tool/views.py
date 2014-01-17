# Create your views here.
import os
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

def financial_info(request):
    i=0
    current_expenses=''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        current_user=request.user
        engineer=EngineerProfile.objects.get(user=current_user)
        project=Project.objects.get(fellow_engineer=engineer)
        
        time=datetime.now()
        month=time.month
        year=time.year
        
        
        if month == 8 or month == 9 or month == 10:
        	quarter_number = 1
        	year=year+1
        if month == 11 or month == 12:
        	quarter_number= 2
        	year=year+1
        if month == 1:
        	quarter_number = 2
        if month == 2 or month == 3 or month == 4:
        	quarter_number = 3
        if month == 5 or month == 6 or month == 7:
        	quarter_number = 4	
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
                    previous_expensestype = ExpensesType.objects.filter(project=project, 
        														quarter_number=4,
        														year=year,
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
                    
                    i=i+1
                return HttpResponseRedirect('/review_info/')
                
        	

    return render(request,'spending_tool/financial_info.html',{'expense_for_current_quarter':expense_for_current_quarter,
    															'previous_expensestype':previous_expensestype,
    															'project':project,
    															'quarter_number':quarter_number
    															})

def add_field(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        current_user=request.user
        engineer=EngineerProfile.objects.get(user=current_user)
        project=Project.objects.get(fellow_engineer=engineer)
        
        time=datetime.now()
        month=time.month
        year=time.year
        
        
        if month == 8 or month == 9 or month == 10:
        	quarter_number = 1
        	year=year+1
        if month == 11 or month == 12:
        	quarter_number= 2
        	year=year+1
        if month == 1:
        	quarter_number = 2
        if month == 2 or month == 3 or month == 4:
        	quarter_number = 3
        if month == 5 or month == 6 or month == 7:
        	quarter_number = 4	
        expense_for_current_quarter=[]

        if request.method == 'POST':
            if quarter_number==1 or quarter_number==2 or quarter_number==3:
                name = request.POST['name']
                expected_cost=request.POST['expected_cost']
                expense_for_next_quarter=ExpensesType.objects.create(year=year,
        										expenses_type=name, 
        										actual_cost=0,
        										estimated_cost=expected_cost,
        										project=project,
        										quarter_number=quarter_number+1,
        										)

                return HttpResponseRedirect('/add_field/')
            if quarter_number==4:
                name= request.POST['name']
                expected_cost=request.POST['expected_cost']
                expense_for_next_quarter=ExpensesType.objects.create(year=year+1,
        										expenses_type=name, 
        										actual_cost=0,
        										estimated_cost=expected_cost,
        										project=project,
        										quarter_number=1,
        										)
                return HttpResponseRedirect('/add_field/')
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

def review_info(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
    	current_user=request.user
        engineer=EngineerProfile.objects.get(user=current_user)
        project=Project.objects.get(fellow_engineer=engineer)
        time=datetime.now()
        year=time.year
        month=time.month
        if month == 8 or month == 9 or month == 10:
            quarter_number = 1
            year=year+1
            previous_quarter=ExpensesType.objects.filter(project=project, year=year-1, quarter_number=4)
        if month == 11 or month == 12:
            quarter_number= 2
            year=year+1
            previous_quarter=ExpensesType.objects.filter(project=project, year=year, quarter_number=1)
        if month == 1:
            quarter_number = 2
            previous_quarter=ExpensesType.objects.filter(project=project, year=year, quarter_number=1)
        if month == 2 or month == 3 or month == 4:
            quarter_number = 3
            previous_quarter=ExpensesType.objects.filter(project=project, year=year, quarter_number=2)
        if month == 5 or month == 6 or month == 7:
            quarter_number = 4
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
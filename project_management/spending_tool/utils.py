from datetime import *
from spending_tool.models import *
import time, threading
from django.http import HttpResponse
from django.core.exceptions import *
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from spending_tool.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as django_logout
from django.template import RequestContext
from spending_tool.forms import *

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

def updateTotal(project):
    #totalExp=projectTotalExpenses.objects.get(project=project)
    #totalExp.funding_approved = project.funding_approved
    totals=ExpensesType.objects.filter(project=project)
    total=0
    for t in totals:
        total=total+t.cross_charge_actual_cost + t.direct_charge_actual_cost
    project.spent_cost=total
    project.save()
    return project.funding_approved, total

def returnExpenses(project):
    cross_charge_actual_cost_specific=direct_charge_actual_cost=[] 
    date = return_quarter_year()
    quarter_number=date[0]
    year=date[1]
    expenses_for_next_quarter=[]
    expenses_for_current_quarter=ExpensesType.objects.filter(
                                                            year=year,
                                                            quarter_number=quarter_number,
                                                            project=project).order_by('expenses_type')
    
    if quarter_number ==2 or quarter_number==3:
        expenses_for_previous_quarter=ExpensesType.objects.filter(
                                                                year=year,
                                                                quarter_number=quarter_number-1,
                                                                project=project).order_by('expenses_type')
        #expenses_for_next_quarter= expenses_for_next_quarter.append(ExpensesType.objects.filter(
        #                                                       year=year,
        #                                                       quarter_number=quarter_number+1,
        #                                                       project=project) )
    if quarter_number==1:
        expenses_for_previous_quarter=ExpensesType.objects.filter(
                                                                year=year-1,
                                                                quarter_number=4,
                                                                project=project).order_by('expenses_type')
        #expenses_for_next_quarter.append(ExpensesType.objects.filter(
        #                                                       year=year,
        #                                                       quarter_number=2,
        #                                                       project=project) )
    if quarter_number==4:
        expenses_for_previous_quarter=ExpensesType.objects.filter(
                                                                year=year,
                                                                quarter_number=quarter_number-1,
                                                                project=project).order_by('expenses_type')
        #expenses_for_next_quarter.append(ExpensesType.objects.filter(
        #                                                       year=year+1,
        #                                                       quarter_number=1,
        #                                                       project=project) )
        
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
    return expenses_for_previous_quarter, expenses_for_current_quarter, expenses_for_next_quarter
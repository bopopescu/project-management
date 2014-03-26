# Create your views here.
import os
'''import xlsxwriter  '''
import csv
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
from datetime import *
from spending_tool.forms import *
from django.contrib.auth.forms import UserCreationForm
from utils import *

# Create your views here.
import smtplib

import re




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
            return HttpResponseRedirect('/login/')
    return render(request, 'spending_tool/login.html', {'username':username, 'password':password})

def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/login/')


def financial_info(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        
        current_user=request.user
        cross_charge_actual_cost_specific=direct_charge_actual_cost=[]
        
        engineer=EngineerProfile.objects.get(user=current_user)
        project=Project.objects.get(fellow_engineer=engineer)
        expenses_for_previous_quarter, expenses_for_current_quarter, expenses_for_next_quarter=returnExpenses(project)
        date = return_quarter_year()
        quarter_number=date[0]
        year=date[1]
        '''
        
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
        '''
        list_for_cross_charge=[]
        current_cross_dept=[]
        for exp in expenses_for_current_quarter:
            if exp.cross_charge_actual_cost>0:
                dept_related_to=DepartmentNumber.objects.filter(relates_to=exp)
                list_for_cross_charge.append((exp, dept_related_to))
                for a in dept_related_to:
                    current_cross_dept.append(a)
        add_dept=request.GET.get('add_dept','')
        if len(add_dept)!=0:
            exp=ExpensesType.objects.get(pk=add_dept)
            DepartmentNumber.objects.create(relates_to=exp,cross_charge_actual_cost=0, department_number=0)
            return HttpResponseRedirect('/financial_info')
        if request.method=='POST':
            i=0
            expected_cost=request.POST.getlist('expected_cost')
            direct_charge_actual_cost=request.POST.getlist('direct_charge_actual_cost')
            cross_charge_actual_cost=request.POST.getlist('cross_charge_actual_cost')

            department_number=request.POST.getlist('department_number')
            cross_charge_actual_cost_specific=request.POST.getlist('cross_charge_actual_cost_specific')
            n=0
            for dept in current_cross_dept:
                dept.department_number=department_number[n]
                dept.cross_charge_actual_cost=cross_charge_actual_cost_specific[n]
                dept.save()
                n=n+1
            actual_cost=request.POST.getlist('actual_cost')
            for expense in expenses_for_current_quarter:
            	expense.direct_charge_actual_cost=direct_charge_actual_cost[i]
                expense.cross_charge_actual_cost=cross_charge_actual_cost[i]
                #expense.department_number=department_number[i]
            	expense.save()
            	expense_for_next_quarter=ExpensesType.objects.get(relates_to=expense)
                expense_for_next_quarter.estimated_cost=expected_cost[i]
                expense_for_next_quarter.save()
            	i=i+1
            return HttpResponseRedirect('/financial_info/')
            
        #info=financialInfo(request)
    return render(request,'spending_tool/financial_info.html',{ 'expenses_for_next_quarter':expenses_for_next_quarter,
    															'expenses_for_current_quarter':expenses_for_current_quarter,
    															'expenses_for_previous_quarter':expenses_for_previous_quarter,
    														    'project':project,
    															'quarter_number':quarter_number,
                                                                'list_for_cross_charge':list_for_cross_charge,
    															'current_cross_dept':current_cross_dept,
                                                                'cross_charge_actual_cost_specific':cross_charge_actual_cost_specific,
                                                                'direct_charge_actual_cost':direct_charge_actual_cost
                                                                })

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
            #department_number=request.POST.get('department_number','')
            cross_charge_actual_cost=request.POST.get('cross_charge_actual_cost','')
            direct_charge_actual_cost=request.POST.get('direct_charge_actual_cost','')
            expected_cost=request.POST['expected_cost']
            current=ExpensesType.objects.create(project=project,
            							expenses_type=name,
            							estimated_cost=expected_cost,
            							cross_charge_actual_cost=cross_charge_actual_cost,
            							direct_charge_actual_cost=direct_charge_actual_cost,
            							year=year,
            							quarter_number=quarter_number,)
            							#department_number=department_number)
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
        total_expenses=ExpensesType.objects.filter(project=project)
        spent_cost=0
        for exp in total_expenses:
            spent_cost=spent_cost+exp.direct_charge_actual_cost+exp.cross_charge_actual_cost
            project.spent_cost=spent_cost
            project.save()
        date=return_quarter_year()
        quarter_number=date[0]
        year=date[1]
        if quarter_number==1:
            previous_quarter=ExpensesType.objects.filter(project=project, year=year-1, quarter_number=4).order_by('expenses_type')
        if quarter_number==2:
            previous_quarter=ExpensesType.objects.filter(project=project, year=year, quarter_number=1).order_by('expenses_type')
        if quarter_number==3:
            previous_quarter=ExpensesType.objects.filter(project=project, year=year, quarter_number=2).order_by('expenses_type')
        if quarter_number==4:
            previous_quarter=ExpensesType.objects.filter(project=project, year=year, quarter_number=3).order_by('expenses_type')
        current_quarter = ExpensesType.objects.filter(project=project, year=year, quarter_number=quarter_number).order_by('expenses_type')
        if quarter_number== 1 or quarter_number==2 or quarter_number == 3:
            next_quarter=ExpensesType.objects.filter(project=project, year=year, quarter_number= quarter_number+1).order_by('expenses_type')
        if quarter_number== 4:
            next_quarter=ExpensesType.objects.filter(project=project, year=year+1, quarter_number= 1).order_by('expenses_type')
        total_exp_current_direct=total_exp_current_cross=total_exp_next_direct=total_exp_next_cross=total_current=0
        for exp in current_quarter:
            total_exp_current_direct=total_exp_current_direct+exp.direct_charge_actual_cost
            total_exp_current_cross=total_exp_current_cross+exp.cross_charge_actual_cost
        
    return render(request,'spending_tool/review_info.html',{'project':project,
    														'quarter_number':quarter_number,
    														'previous_quarter':previous_quarter,
    													 	'current_quarter':current_quarter,
    													 	'next_quarter':next_quarter,
                                                            'total_exp_current_direct':total_exp_current_direct,
                                                            'total_exp_current_cross':total_exp_current_cross,
                                                            'spent_cost':spent_cost})



def edit_status(request):
    time=datetime.now()
    today=time
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        current_user = request.user
        engineer = EngineerProfile.objects.get(user=current_user)
        project = Project.objects.get(fellow_engineer=engineer)
        previous_status=DescriptionType.objects.filter(project=project).order_by('date')
        l=len(previous_status)
        index=l-1
        one_status=previous_status[index]
        previous_status=previous_status[:index]
        quarter_number=return_quarter_year()[0]
        year=return_quarter_year()[1] 
        if request.method == 'POST':
            recent_accomplishments=request.POST['recent_accomplishments']
            current_challenges=request.POST['current_challenges']
            next_steps=request.POST['next_steps']
            DescriptionType.objects.create(project=project,
                                           quarter_number=quarter_number,
                                           year=year,
                                           date=time,
                                           recent_accomplishments=recent_accomplishments,
                                           next_steps=next_steps,
                                           current_challenges=current_challenges
                )
   
            return HttpResponseRedirect('/edit_status/')              
    return render(request, 'spending_tool/edit_status.html',{'project':project, 
                                                             'quarter_number':quarter_number,
                                                             'one_status':one_status,
                                                             'today':today,
                                                             'previous_status':previous_status})


def edit(request):
    time=datetime.now()
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        current_user = request.user
        id_status=request.GET['status']
        engineer = EngineerProfile.objects.get(user=current_user)
        project = Project.objects.get(fellow_engineer=engineer)
        current_status=DescriptionType.objects.get(pk=id_status)
        quarter_number=return_quarter_year()[0]
        if request.method == 'POST':
            current_status.recent_accomplishments=request.POST['recent_accomplishments']
            current_status.current_challenges=request.POST['current_challenges']
            current_status.next_steps=request.POST['next_steps']
            current_status.save()
            return HttpResponseRedirect('/edit_status')
    return render(request, 'spending_tool/edit.html', {'project':project, 'quarter_number':quarter_number, 'current_status':current_status})


def status(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        current_user = request.user
        engineer = EngineerProfile.objects.get(user=current_user)
        project = Project.objects.get(fellow_engineer=engineer) 
  
  # This needs to change .... 

        description = DescriptionType.objects.filter(project=project)  

        if request.method == 'GET':
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
        if request.method == 'POST':
            form = ProjectsummaryForm(request.POST or None, instance=request.user.get_profile())
            if form.is_valid():
                form.save()
                new_user = form.save()
                return HttpResponseRedirect('/project_summary/')
        else:
            form = ProjectsummaryForm(instance = request.user.get_profile())
    return render(request, 'spending_tool/project_summary.html',{'project':project,'form':form})

def input_milestones(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        current_user = request.user
        engineer = EngineerProfile.objects.get(user=current_user)
        project = Project.objects.get(fellow_engineer=engineer)
        previous_milestones = Milestone.objects.filter(project=project).order_by('due_date')
        quarter_number=return_quarter_year()[0]
        today=datetime.today()
        year=return_quarter_year()[1]
        if request.method == 'POST':
            try:
                due_date=request.POST['date']
                percentage=request.POST['percentage']
                schedule=request.POST['schedule']
                Milestone.objects.create( 
                                      date=today,
                                      due_date=due_date,
                                      major_milestone=schedule,
                                      percentage_complete=percentage,
                                      project=project,
                                      quarter_number=quarter_number,
                                      year=year,

                )
            except ValidationError:
                pass
            return HttpResponseRedirect('/input_milestones/')              
    return render(request, 'spending_tool/input_milestones.html',{'quarter_number':quarter_number ,'project':project,'previous_milestones':previous_milestones})

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
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        current_user = request.user
        engineer = EngineerProfile.objects.get(user=current_user)
        project = Project.objects.get(fellow_engineer=engineer) 
        if request.method == 'POST':
            form = DetailsForm(request.POST or None, instance=project)
            if form.is_valid():
                #form.save()
                new_user = form.save()
                return HttpResponseRedirect('/project_details/')
        else:
            form = DetailsForm(instance = project) 
    return render(request, 'spending_tool/project_details.html',{'project':project,'form':form})


def attach_document(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        current_user = request.user
        engineer = EngineerProfile.objects.get(user=current_user)
        project = Project.objects.get(fellow_engineer=engineer)
        documents=Document.objects.filter(project=project)
        if request.method == 'POST':
           form = UploadFileForm(request.POST, request.FILES)
           if form.is_valid():
               time=datetime.now()

            # file is saved
               new_document=form.save(commit = False)
               new_document.project=project
               new_document.date=time
               new_document.save()
               return HttpResponseRedirect('/attach_document/')
        else:
           form = UploadFileForm()
    return render(request,'spending_tool/attach_document.html',{'project':project, 'form':form, 'documents':documents})

def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        current_user = request.user
        engineer = EngineerProfile.objects.get(user=current_user)
        project = Project.objects.get(fellow_engineer=engineer)
    return render(request,'spending_tool/home.html',{'project':project})
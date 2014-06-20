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
from datefunction import return_quarter_year
# Create your views here.
import smtplib

import re

import xlsxwriter
date = return_quarter_year()
quarter_number=date[0]
year=date[1]
'''
def create_tmp_project(request):
    project_id=request.GET.get('id')
    tmProject.objects.create(project_id=project_id)
    return HttpResponseRedirect('/financial_info/')  
'''
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

def home(request):
    list_active_projects=Project.objects.filter(status='Active').order_by('name_project')
    list_completed_projects=Project.objects.filter(status='Complete').order_by('name_project')
    return render(request,'spending_tool/home.html', {'list_active_projects':list_active_projects,
                                                      'list_completed_projects':list_completed_projects})

def guidelines(request):
    project_id=request.GET.get('id')
    if project_id is None or len(project_id)==0:
        return HttpResponseRedirect('/home/')
    else:
        project=Project.objects.get(pk=project_id)  
        return render(request,'spending_tool/guidelines.html', {'project':project})

def financial_info(request):
    project_id=request.GET.get('id')
    if project_id is None or len(project_id)==0:
        return HttpResponseRedirect('/home/')
    else:
        try: 
            current_user=request.user
            cross_charge_actual_cost_specific=direct_charge_actual_cost=[]
            #engineer=EngineerProfile.objects.get(user=current_user)
            project=Project.objects.get(pk=project_id)
            expenses_for_previous_quarter, expenses_for_current_quarter, expenses_for_next_quarter=returnExpenses(project)
            date = return_quarter_year()
            quarter_number=date[0]
            year=date[1]
            month=date[2]
            list_for_cross_charge=[]
            current_cross_dept=[]
            for exp in expenses_for_current_quarter:
                if exp.cross_charge_actual_cost>0:
                    dept_related_to=DepartmentNumber.objects.filter(relates_to=exp)
                    sum_depts=0
                    for d in dept_related_to:
                        sum_depts=sum_depts+d.cross_charge_actual_cost
                    res=exp.cross_charge_actual_cost-sum_depts
                    list_for_cross_charge.append((exp, dept_related_to, sum_depts,res ))
                    for a in dept_related_to:
                        current_cross_dept.append(a)
            add_dept=request.GET.get('add_dept','')
            if len(add_dept)!=0:
                exp=ExpensesType.objects.get(pk=add_dept)
                DepartmentNumber.objects.create(relates_to=exp,cross_charge_actual_cost=0, department_number=0)
                return HttpResponseRedirect('/financial_info/?id='+project_id)
            if request.method=='POST':
                i=0
                expected_cost=request.POST.getlist('expected_cost')
                direct_charge_actual_cost=request.POST.getlist('direct_charge_actual_cost')
                cross_charge_actual_cost=request.POST.getlist('cross_charge_actual_cost')

                department_number=request.POST.getlist('department_number')
                person=request.POST.getlist('person')
                cross_charge_actual_cost_specific=request.POST.getlist('cross_charge_actual_cost_specific')
                n=0
                for dept in current_cross_dept:
                    dept.department_number=department_number[n]
                    dept.cross_charge_actual_cost=cross_charge_actual_cost_specific[n]
                    dept.person=person[n]
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
                return HttpResponseRedirect('/financial_info/?id='+project_id)               
        except ValidationError:
            pass   

        #info=financialInfo(request)
        updateTotal(project)
        total_current_direct, total_current_cross=returnTotal(expenses_for_current_quarter)
        totalExp=projectTotalExpenses.objects.get(project=project)
    return render(request,'spending_tool/financial_info.html',{ 'expenses_for_next_quarter':expenses_for_next_quarter,
    															'expenses_for_current_quarter':expenses_for_current_quarter,
    															'expenses_for_previous_quarter':expenses_for_previous_quarter,
    														    'project':project,
                                                                'totalExp':totalExp,
                                                                'year':year,
                                                                'month':month,
                                                                'total_current_direct':total_current_direct,
                                                                'total_current_cross':total_current_cross,
    															'quarter_number':quarter_number,
                                                                'list_for_cross_charge':list_for_cross_charge,
    															'current_cross_dept':current_cross_dept,
                                                                'cross_charge_actual_cost_specific':cross_charge_actual_cost_specific,
                                                                'direct_charge_actual_cost':direct_charge_actual_cost
                                                                })

def add_field(request):
    project_id=request.GET.get('id')
    if project_id is None or len(project_id)==0:
        return HttpResponseRedirect('/home/')
    else:
        current_user=request.user

        #engineer=EngineerProfile.objects.get(user=current_user)
        project=Project.objects.get(pk=project_id)
        
        date=return_quarter_year()
        quarter_number=date[0]
        year=date[1]

        expense_for_current_quarter=[]

        if request.method == 'POST':
            try:
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
            except ValidationError:
                pass
            return HttpResponseRedirect('/financial_info/?id='+project_id)
            
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
        
    return render(request,'spending_tool/add_field.html',{'quarter_number':quarter_number,
                                                          'year':year,
                                                          'project':project, 
                                                          'expense_for_current_quarter':expense_for_current_quarter})


def add_current_field(request):
    project_id=request.GET.get('id')
    if project_id is None or len(project_id)==0:
        return HttpResponseRedirect('/home/')
    else:  
        current_user=request.user

        #engineer=EngineerProfile.objects.get(user=current_user)
        project=Project.objects.get(pk=project_id)
        
        date=return_quarter_year()
        quarter_number=date[0]
        year=date[1]
        if request.method=='POST':
            try:
                name = request.POST['name']
                #department_number=request.POST.get('department_number','')
                cross_charge_actual_cost=request.POST.get('cross_charge_actual_cost','')
                direct_charge_actual_cost=request.POST.get('direct_charge_actual_cost','')
                expected_cost=0 #request.POST.get('expected_cost','')
                current=ExpensesType.objects.create(project=project,
                							expenses_type=name,
                							estimated_cost=expected_cost,
                							cross_charge_actual_cost=cross_charge_actual_cost,
                							direct_charge_actual_cost=direct_charge_actual_cost,
                							year=year,
                							quarter_number=quarter_number,)
                							#department_number=department_number)
            except ValidationError:
                return HttpResponseRedirect('/add_current_field/?id='+project_id)
            return HttpResponseRedirect('/financial_info/?id='+project_id)
    return render(request,'spending_tool/add_current_field.html',{'quarter_number':quarter_number,
                                                                  'year':year,
                                                                  'project':project})



def review_info(request):
    project_id=request.GET.get('id')
    if project_id is None or len(project_id)==0:
        return HttpResponseRedirect('/home/')
    else:  
    	current_user=request.user
        #engineer=EngineerProfile.objects.get(user=current_user)
        project=Project.objects.get(pk=project_id)
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
                                                            'year':year,
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
    project_id=request.GET.get('id')
    if project_id is None or len(project_id)==0:
        return HttpResponseRedirect('/home/')
    else:  
        #current_user = request.user
        #engineer = EngineerProfile.objects.get(user=current_user)
        project = Project.objects.get(pk=project_id)
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
   
            return HttpResponseRedirect('/edit_status/?id='+str(project.id))              
    return render(request, 'spending_tool/edit_status.html',{'project':project, 
                                                             'year':year,
                                                             'quarter_number':quarter_number,
                                                             'one_status':one_status,
                                                             'today':today,
                                                             'previous_status':previous_status})


def edit(request):
    time=datetime.now()
    project_id=request.GET.get('id')
    if project_id is None or len(project_id)==0:
        return HttpResponseRedirect('/home/')
    else:  
        #current_user = request.user
        id_status=request.GET['status']
        #engineer = EngineerProfile.objects.get(user=current_user)
        project = Project.objects.get(pk=project_id)
        current_status=DescriptionType.objects.get(pk=id_status)
        quarter_number=return_quarter_year()[0]
        if request.method == 'POST':
            current_status.recent_accomplishments=request.POST['recent_accomplishments']
            current_status.current_challenges=request.POST['current_challenges']
            current_status.next_steps=request.POST['next_steps']
            current_status.save()
            return HttpResponseRedirect('/edit_status/?id='+project_id)
    return render(request, 'spending_tool/edit.html', {'project':project, 
                                                       'year':year,
                                                       'quarter_number':quarter_number,
                                                       'current_status':current_status})


def status(request):
    project_id=request.GET.get('id')
    if project_id is None or len(project_id)==0:
        return HttpResponseRedirect('/home/')
    else:  
        #current_user = request.user
        #engineer = EngineerProfile.objects.get(user=current_user)
        project = Project.objects.get(pk=project_id) 
  
  # This needs to change .... 

        description = DescriptionType.objects.filter(project=project)  

        if request.method == 'GET':
            recent_accomplishments = description.recent_accomplishments
            current_challenges = description.current_challenges
            next_steps = description.next_steps
              
    return render(request, 'spending_tool/status.html',{'project':project,
                                                        'year':year, 
                                                        'recent_accomplishments':recent_accomplishments,
                                                        'current_challenges':current_challenges,
                                                        'next_steps':next_steps})

def project_summary(request):
    project_id=request.GET.get('id')
    if project_id is None or len(project_id)==0:
        return HttpResponseRedirect('/home/')
    else:  
        #current_user = request.user
        #engineer = EngineerProfile.objects.get(user=current_user)
        project = Project.objects.get(pk=project_id) 
        if request.method == 'POST':
            form = ProjectsummaryForm(request.POST or None, instance=project)
            if form.is_valid():
                #form.save()
                new_user = form.save()
                return HttpResponseRedirect('/project_summary/?id='+project_id)
        else:
            form = ProjectsummaryForm(instance = project)
    return render(request, 'spending_tool/project_summary.html',{'project':project,
                                                                 'year':year,
                                                                 'form':form})

def input_milestones(request):
    project_id=request.GET.get('id')
    if project_id is None or len(project_id)==0:
        return HttpResponseRedirect('/home/')
    else:  
        #current_user = request.user
        #engineer = EngineerProfile.objects.get(user=current_user)
        project = Project.objects.get(pk=project_id)
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
            return HttpResponseRedirect('/input_milestones/?id='+project_id)              
    return render(request, 'spending_tool/input_milestones.html',{'quarter_number':quarter_number ,
                                                                  'year':year,
                                                                  'project':project,
                                                                  'previous_milestones':previous_milestones})

def milestones(request):
    project_id=request.GET.get('id')
    if project_id is None or len(project_id)==0:
        return HttpResponseRedirect('/home/')
    else:  
        #current_user = request.user
        #engineer = EngineerProfile.objects.get(user=current_user)
        project = Project.objects.get(pk=project_id)
        description = DescriptionType.objects.get(project=project)  
        major_milestone = description.major_milestone
        due_date = description.due_date
        percentage_complete = description.percentage_complete
    return render(request, 'spending_tool/milestones.html',{'project':project,
                                                            'major_milestone':major_milestone,
                                                            'year':year,
                                                            'due_date':due_date,
                                                            'quarter_number':quarter_number ,
                                                            'percentage_complete':percentage_complete})

def project_details(request):
    project_id=request.GET.get('id')
    if project_id is None or len(project_id)==0:
        return HttpResponseRedirect('/home/')
    else:  
        #current_user = request.user
        #engineer = EngineerProfile.objects.get(user=current_user)
        project = Project.objects.get(pk=project_id) 
        if request.method == 'POST':
            form = DetailsForm(request.POST or None, instance=project)
            if form.is_valid():
                #form.save()
                new_user = form.save()
                return HttpResponseRedirect('/project_details/?id='+project_id)
        else:
            form = DetailsForm(instance = project) 
    return render(request, 'spending_tool/project_details.html',{'project':project,
                                                                 'quarter_number':quarter_number ,
                                                                 'form':form,
                                                                 'year':year,})


def attach_document(request):
    project_id=request.GET.get('id')
    if project_id is None or len(project_id)==0:
        return HttpResponseRedirect('/home/')
    else:  
        #current_user = request.user
        #engineer = EngineerProfile.objects.get(user=current_user)
        project = Project.objects.get(pk=project_id)
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
               return HttpResponseRedirect('/attach_document/?id='+project_id)
        else:
           form = UploadFileForm()
    return render(request,'spending_tool/attach_document.html',{'project':project,
                                                                'form':form,
                                                                'year':year,
                                                                'quarter_number':quarter_number ,
                                                                'documents':documents})



def create_report(request):
    project_id=request.GET.get('id')
    if project_id is None or len(project_id)==0:
        return HttpResponseRedirect('/home/')
    else:  
        #current_user = request.user
        #engineer = EngineerProfile.objects.get(user=current_user)
        project = Project.objects.get(pk=project_id)
        try:
            import cStringIO as StringIO
        except ImportError:
            import StringIO
        output = StringIO.StringIO()
        title=str(project.name_project)
        #workbook=xlsxwriter.Workbook('report_%s.xlsx' %(queryset.test))    
        workbook=xlsxwriter.Workbook(output)
        #workbook=xlsxwriter.Workbook('blablabla.xlsx')
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        time=datetime.now()
        year=time.year
        list_quarters=[]
        #project_id=queryset.id
        line=2
        cell=0
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
        return response

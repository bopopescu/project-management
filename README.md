TECH FUND FINANCE Documentation
----------------------

**Introduction**

  Tech Fund Finance is a Django app used to record quarterly expenses for Cisco Tech Funded projects. Each quarter the project owner is able to enter the amount for each expense and enter an estimate for next quarter. The tool also allows the project owners to manage their project by entering quarterly milestones, status's and generating reports.
  
===================================================================

SECTION 1:
----------

The web app has been built using the Django framework and is currently hosted on an internal Cisco VM. If you have never used Django please follow the tutorial at https://docs.djangoproject.com/en/1.5/intro/tutorial01/ . The Django version used here is 1.5.4

The OS we suggest is Ubuntu 12.04 and all the following instructions that you will see assume that you are using Ubuntu 12.04. 

1.The Set-Up:
-------------
Firstly let's setup our enviroment in order to have Django ready.

a. Install pip
```
$ sudo apt-get install python-pip
```
b. Install Django
```
$ pip install django>=1.4   (May require: $ sudo pip install Django)
```
c. Install PostgreSQL
```
$ apt-get install postgresql-9.3
```
d. Install the psycopg2 driver for PostgreSQL
```
$ sudo easy_install psycopg2
```
c. Clone the repo
```
$ git clone git:git@github.com:fraferra/project-management.git
```
2.Familiarazing with Django 1.5.4
--------
**OVERVIEW**

We used a Model–view–controller (MVC) architecture. The structure of every object is defined in /spending_tool/models.py. /spending_tool/views.py controls the views and the requests of the users and in /spending_tool/templates/spending_tool/ you will find all the templates used. For help understanding the template tags used in Django visit http://jinja.pocoo.org/docs/templates/.

In the folder project_management you will find settings.py; spending_tool is the actual Django app.

/spending_tool/
------

This is the actual app, where all the models, the views and the controller are.

**The Models**

  In models.py you will find all the objects used in Tech Fund Finance. Each field describes a property of the object.
  
  **ATTENTION:** If you change a field in models make sure to create a new database afterward to update from your old database schema to your new database structure. Then run:

  $ python manage.py syncdb
  ```

**The Controller**

  In views.py you will find all the logic that handles the different requests. 
  In every method we handle a different request. 
  
**The Views**

  In /templates/spending_tool/ you will find all the templates that define the views, familiarize on the way we pass variables from the controller to the view. If we pass a variable, eg. x,  then we render the page and will use {{ x }} within a template.
  
**Other files**
  
  **Urls.py**
 
  urls.py, as you can guess from the name it's where we link the actual URL of a page to method in our views.py
  
  **Forms.py**
  
  A form in django is used to enter info about an object defined in models.py. In forms.py each class defines a form. You will need to define which object the form is linked to and the fields that you want to display. You can also style the fields if you define the form fields directly in the form. Have a look at this link for further info about forms: https://docs.djangoproject.com/en/1.5/topics/forms/ 

  **Admin.py**

  admin.py is used to configure the Django Admin interface. You need to edit admin.py if you want to change the information displayed about the objects in the Django Admin.
  
  **datefunction.py**
  
  

  **create_report.py**


  
/project_management/
--------

This is where the settings are, you rarely touch the files in /settings.py/.

========================================================================================
  
SECTION 2 (UPDATING THE CONTENT):
----------------

**Overview**

This webapp does not have a CMS (Content Management System), hence all the changes must be done directly in the templates.

If you have a basic knowledge of HTML then you should be able to change the contents with no problem.

Below there is a short 'map' of the templates and what contents they contain.


**THE CONTENT MAP**

* /spending_tool/templates/spending_tool/home.html -- homepage with list of active and completed tech fund projects

* /spending_tool/templates/spending_tool/financial_info.html -- enter quarterly expenses

* /spending_tool/templates/spending_tool/add_current_field.html -- add expense for current quarter

* /spending_tool/templates/spending_tool/review_info.html -- review expenses tables

* /spending_tool/templates/spending_tool/project_summary.html -- project summary

* /spending_tool/templates/spending_tool/project_details.html -- project details

* /spending_tool/templates/spending_tool/edit_status.html -- enter quarterly status of project

* /spending_tool/templates/spending_tool/edit.html -- edit a previous status

* /spending_tool/templates/spending_tool/input_milestones.html -- enter quarterly milestones

* /spending_tool/templates/spending_tool/attach_document.html -- attach document to project

* /spending_tool/templates/spending_tool/guidelines.html -- guidelines for tool

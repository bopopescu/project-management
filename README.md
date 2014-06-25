TECH FUND FINANCE Documentation
----------------------

**Introduction**

  Tech Fund Finance is a Django app to automate how expenses are entered for Tech Fund projects. The tool allows the user to enter Direct and Cross Charges for expenses each quarter. At the same time users can enter details about thr project as well as entering quarterly milestones and statuses.
  
===================================================================

SECTION 1 (CODERS):
----------

**THE PHILOSOPHY:**
The web app has been built using the Django framework and is currently hosted on an internal Cisco VM ... If you have never used Django please follow the tutorial at https://docs.djangoproject.com/en/1.5/intro/tutorial01/ . The Django version used here is 1.5.4

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
$ pip install Django   (May require: $ sudo pip install Django)
```

c. Install PostgreSQL
```
$ apt-get install postgresql-9.3
```

d. Install the psycopg2 driver for PostgreSQL
```
$ sudo easy_install psycopg2
```
2.Familiarazing with Django 1.5.4
--------
**OVERVIEW**

We used a Model–view–controller (MVC) architecture. The structure of every object is defined in /spending_tool/models.py. /spending_tool/views.py controls the views and the requests of the users and in /spending_tool/templates/spending_tool/ you will find all the templates used. For help understanding the template tags used in Django visit http://jinja.pocoo.org/docs/templates/.

In the folder project_management you will find settings.py; spending_tool is the actual Django app.

/spending_tool/
------

This is actual app, where all the models, the views and the controller are.

**The Models**

  In models.py you will find all the objects used in Tech Fund Finance. Each field describes a property of the object.
  
  **ATTENTION:** If you change a field in models make sure to create a new database afterward to update from your old database schema to your new database structure. Look at the section PostgreSQL in this documentation to see how to do it.

**The Controller**

  In views.py you will find all the logic that handles the different requests. 
  In every method we handle a different requests. Some of the backend logic is then process in functions.py
  
**The Views**

  In /templates/spending_tool/ you will find all the templates that define the views, familiarize on the way we pass variables from the controller to the view ( we pass a variable, eg. x,  when we render the page and then we use {{ x }} within a template.
  
**Other files**
  
  **Urls.py**
 
  urls.py, as you can guess from the name it's where we link the actual URL of a page to method in our views.py
  
  **Forms.py**
  
  A form in django is used to enter info about an object define in the models. It is used for two main reasons:
  
  1- it's quicker, in fact you don't have to write HTML, you just need to pass the form to the templates
  
  2- It handles user's errors, in fact a form will not validate if, for instance, a user enter a string in a field in which there should be an integer.
  
  In forms.py each class defines a form. You will need to define which object thet form is linked to and the fields that you want to display. You can also style the fields if you define the form fields directly in the form. Have a look at this link for further info about forms: https://docs.djangoproject.com/en/1.5/topics/forms/ 

  **Admin.py**

  admin.py is used to configure the Django Admin interface. You need to edit admin.py if you want to change the informations displayed about the objects in the Django Admin.
  
  **Functions.py**
  
  In this file you will find some recurrent functions used in the backend
  
/mysite/
--------

This is where the settings are, you rarely touch the files in /mysite/.


POSTGRESQL
-----

**OVERVIEW**



========================================================================================
  
SECTION 2 (UPDATING THE CONTENT):
----------------

**Overview**

This webapp does not have a CMS (Content Management System), hence all the changes must be done directly in the templates.

If you have a basic knowledge of HTML then you should be able to change the contents with no problem.

Below there is a short 'map' of the templates and what contents they contain.


**THE CONTENT MAP**


'''
Created on Jul 22, 2012

@author: paul

This module defines the datastore structure
'''

from google.appengine.ext import db

#Information structure of registered domains' entities
class Student(db.Model):
    username = db.StringProperty()
    department = db.StringProperty()
    response_flag = db.StringProperty()

class Super_Admins(db.Model):
    emailAddress = db.StringProperty()
    active = db.BooleanProperty()

class Quality_Assurance(db.Model):
    emailAddress = db.StringProperty()
    active = db.BooleanProperty()
    
class Dept_Admins(db.Model):
    emailAddress = db.StringProperty()
    department =  db.StringProperty()
    active = db.StringProperty()
    
class Departments(db.Model):
    departmentName = db.StringProperty()
    active = db.StringProperty()
    


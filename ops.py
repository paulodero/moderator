'''
Created on Jul 22, 2012

@author: paul

This module contains functions defined in the application
'''
import models

from google.appengine.api import users

#Functions to get data from the datastore
#A function to get details of a particular sub-domain sub-domain
def getStudent(reg_no):
    q = models.Student().all().filter('password =', reg_no)
    row = q.fetch(1)
    return row

#get Departments
def getDepartments():
    q = models.Departments().all()
    row = q.fetch(100)
    return row

#A function to get domain from an email address
def getDomainFromEmail(email):
    emailarr = email.split('@')
    subdomain = emailarr[1]
    return subdomain

#A function to get domain from a sub-domain
def getDomainFromSubdomain(subdomain):
    emailarr = subdomain.split('.')
    domain = emailarr[1]
    return domain

#Get username from email
def getUserNameFromMail(email):
    emailarr = email.split('@')
    return emailarr[0]

def getData(department):
    q = models.Student.all().filter('department =', department).filter('response_flag = ', '1')
    return q
                           
#Add department
def addDepartment(department):        
    row = models.Departments(key_name = addUnderscore(department))
    row.active = '1'
    row.departmentName = addUnderscore(department)#department_name
    row.put()

#Add Admins
def addAdmins(department,email_address):
    key = '%s_%s' % (department,email_address)
    row = models.Dept_Admins(key_name = key)
    row.department = department
    row.emailAddress = email_address
    row.active = '1'
    row.put()

def addUnderscore(theword):
    departmentArr = theword.split(' ')
    department_name = ''
    count = 0
    for word in departmentArr:
        if count == 1:
            department_name += '_'
        department_name += word
        count = 1
    return department_name

#Add Student
def AddStudent(department, email):
    row = models.Student(key_name = email)
    row.username = getUserNameFromMail(email)
    row.response_flag = '1'
    row.department = department
    row.put()
    
#Update student response flag
def updateStudent(offset):
    q = models.Student.all().filter('response_flag =', '1')
    rows = q.fetch(10,offset)    
    for row in rows:
        row.response_flag = '0'
        row.put()
    q = models.Student.all().filter('response_flag =', '1')
    row = q.fetch(1)
    offset = offset + 1000
    if row:
        updateStudent(offset)
        
def addQA(email):
    row = models.Quality_Assurance(key_name = email)
    row.emailAddress = email
    row.active = True
    row.put()    
    
def getCurrentUserEmail():
    user = users.get_current_user()
    email_Address = user.email()
    
    return email_Address

#Sorting data in csv
def sortcsvdata(data):
    dictValues = {}
    for value in data:
        username = str(value.username)
        dictValues[username] = value
    keys = dictValues.keys()
    keys.sort()
    sortedListValues = map(dictValues.get, keys)
    return sortedListValues
  
def removeUnderscores(thestrings):
    stringArr = thestrings.split('_')
    string = ''
    count = 0
    for word in stringArr:
        if count == 1:
            string += ' '
        string += word
        count = 1
    return string

def removeDept(department):
    q = models.Departments.all().filter('department  =', department)
    row = q.fetch(1)
    row.active = '0'
    row.put()

def isQA(email):
    q = models.Quality_Assurance.all().filter('emailAddress =', email)
    rows = q.fetch(1)
    if rows:
        return True    
    return False

def isAdmin(email):
    q = models.Dept_Admins.all().filter('emailAddress =', email)
    rows = q.fetch(1)
    if rows:
        return True
    return False

def isSuperAdmin(email):
    q = models.Super_Admins.all().filter('emailAddress =', email)
    rows = q.fetch(1)
    if rows:
        return True
    return False
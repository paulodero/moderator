'''
Created on Oct 15, 2012

@author: paul
'''
from google.appengine.ext import webapp

register = webapp.template.create_template_register()
#Remove spaces in a string
def removeSpacesInString(thestrings):
    thestringsarr = thestrings.split()
    string = ''
    for thestring in thestringsarr:
        string += thestring
    return string

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

register.filter(removeSpacesInString)
register.filter(removeUnderscores)

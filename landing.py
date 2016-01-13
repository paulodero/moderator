'''
Created on Jul 19, 2015

@author: paul
'''

import os
import ops
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from settings import TEMPLATES_PATH
from google.appengine.ext.webapp import util


DIRECTORY = os.path.dirname(__file__)
_DEBUG = True
values = {}
fill_flag = 0


webapp.template.register_template_library('tags.filters')

#Landing Page handler
class LandingPage(webapp.RequestHandler):
    #Render the landing page handler
    def get(self):
        user = users.get_current_user()
        if user:
            email = user.email()
            subdomain = ops.getDomainFromEmail(email)
            isQualityAssurance = ops.isQA(email)
            isAdmin = ops.isAdmin(email)
            isSuperAdmin = ops.isSuperAdmin(email)
            if subdomain != 'jkuat.ac.ke':
                domain = ops.getDomainFromSubdomain(subdomain)
                if domain != 'jkuat':
                    self.redirect('/unauthorized')
            values = defaultValues()
            values['isQualityAssurance'] =  isQualityAssurance
            values['isAdmin'] = isAdmin
            values['isSuperAdmin'] = isSuperAdmin
            wireframe = 'registerDepartment'
        else :
            wireframe = 'unauthorised'
            values =  {}
            values['login_url'] = users.create_login_url('/')
        app_path = os.path.join(DIRECTORY, os.path.join('templates', '%s.html' % wireframe))
        values['app'] = template.render(app_path, values, debug=_DEBUG)
        path = os.path.join(TEMPLATES_PATH,'main.html')
        self.response.out.write(template.render(path, values, debug=_DEBUG))

#Render various application views
class ViewHandler(webapp.RequestHandler):
    def get(self):
        view_info = self.request.path_info.split('/')
        user = users.get_current_user()
        email = user.email()
        values = defaultValues()
        isQualityAssurance = ops.isQA(email)
        isAdmin = ops.isAdmin(email)
        isSuperAdmin = ops.isSuperAdmin(email)
        values = defaultValues()
        values['isQualityAssurance'] =  isQualityAssurance
        values['isAdmin'] = isAdmin
        values['isSuperAdmin'] = isSuperAdmin
        if len(view_info)<2:
            return
        view = view_info[1]
        if view == 'student_details':
            reg_no = self.request.get('regno',None)         
            values['student_details'] = ops.getStudent(reg_no)
            if len(values['student_details']) > 0:
                wireframe = 'student_details'
            else:
                wireframe = 'record_notfound'    
                                     
            values['title'] = 'Kisii University'
            values['regno'] = reg_no
            
        elif view == 'unauthorized':
            wireframe = 'unauthorized'
        elif view == 'add_admin':
            wireframe = 'addadmin'
        elif view == 'remove_admin':
            wireframe = 'removeAdmin'
        elif view == 'add_dept':
            wireframe = 'addDept'
        elif view == 'retrieveStudents':
            wireframe = 'downloadStudents'
        elif view == 'remove_dept':
            wireframe = 'removeDept'
        elif view == 'addDepartment':
            department_name = self.request.get('department', None)
            ops.addDepartment(department_name)
            wireframe = 'recordAdded'
        elif view == 'addAdministrator':
            department_name = self.request.get('department', None)
            emailAddress = self.request.get('emailAddress', None)
            ops.addAdmins(department_name, emailAddress)
            wireframe = 'recordAdded'
        elif view == 'home':
            department_name = self.request.get('department', None)
            ops.AddStudent(department_name,values['nickname'])
            wireframe = 'home'
        elif view == 'removeDepartment':
            department_name = self.request.get('department', None)
            ops.removeDept(department_name)
            wireframe = 'recordAdded'            
        elif view == 'add_QA':
            wireframe = 'addQA'         
        elif  view == 'addQualityAssurance':
            emailAddress = self.request.get('emailAddress', None)
            ops.addQA(emailAddress)
            wireframe = 'recordAdded'
        elif view == 'updateStudent':
            ops.updateStudent(0)
            wireframe = 'recordAdded'
                
                                               
        app_path = os.path.join(TEMPLATES_PATH,'%s.html' % wireframe)
        values['app'] = template.render(app_path, values, debug=_DEBUG)
        path = os.path.join(TEMPLATES_PATH,'main.html')
        self.response.out.write(template.render(path, values, debug=_DEBUG))


def defaultValues():
    user = users.get_current_user()
    nickname = user.nickname()
    logout_url = users.create_logout_url('/')
    institution = "jkuat University"
    departments = ops.getDepartments()

    return  {
                          
                    'owner': user.email(),
                    'nickname': nickname,
                    'logout_url': logout_url,
                    'institution': institution,
                    'departments': departments,
                     'isQualityAssurance': False,
                     'isAdmin': False,
                     'isSuperAdmin': False
                  } 


        
def main():
    application = webapp.WSGIApplication([('/',LandingPage),
                                         ('/student_details',ViewHandler),
                                         ('/view/.*',ViewHandler),
                                         ('/unauthorized',ViewHandler),
                                          ('/add_admin',ViewHandler),
                                           ('/remove_admin',ViewHandler),
                                           ('/add_dept',ViewHandler),
                                           ('/recordAdded',ViewHandler),
                                           ('/addDepartment',ViewHandler),
                                           ('/.*',ViewHandler)],debug = True)
    util.run_wsgi_app(application)
if __name__ == "__main__":
    main()

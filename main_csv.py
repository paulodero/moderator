'''
Created on 9 Jul 2014

@author: podero

This module generated csv files to be downloaded from the portal.
'''
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import ops

class MainPage(webapp.RequestHandler):   
  def get(self):
    department = self.request.get('department',None)
    data = ops.sortcsvdata(ops.getData(department))
    self.response.headers['Content-Type'] = 'text/csv'
    self.response.headers['Content-Disposition'] = "attachment; filename=%s.csv"  % (department)
    
    self.response.out.write(','.join(['Department','Username']))
    for row in data:
      self.response.out.write(','.join(['\n']))
      self.response.out.write(','.join([str(ops.removeUnderscores(row.department)),'']))
      self.response.out.write(','.join([str(row.username),'']))
def main():
  application = webapp.WSGIApplication([('/csv', MainPage)], debug=True)
  run_wsgi_app(application)
if __name__ == "__main__":
    main()

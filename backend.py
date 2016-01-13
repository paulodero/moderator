'''
Created on Jun 12, 2014

@author: podero
'''
# App Engine API (works with both HTTP GET and POST requests):
# To echo request parameters:
#   http://hugo-test.appspot.com/rpc?action=Echo&params={"key":"a","value":"xxx"}&key=mySecretKey
# Returns: {"value": "xxx", "key": "a"}
# To compute the square of a number:
#   http://hugo-test.appspot.com/rpc?action=Square&params={"value":11}&key=mySecretKey
# Returns: {"value": 121}
# To store a key value pair:
#   http://hugo-test.appspot.com/rpc?action=Store&params={"key":"a","value":"xxx"}&key=mySecretKey
# Returns: {"retCode": "Ok"}
# To lookup value by key:
#   http://hugo-test.appspot.com/rpc?action=Lookup&params={"key":"a"}&key=mySecretKey
# Returns: {"retCode": "Ok", "value": "xxx"}

import json
import webapp2
import ops

from google.appengine.ext import db
from google.appengine.api import users


class RPCMethods:
  """ Defines the methods that can be RPCed.
  NOTE: Do not allow remote callers access to private/protected "_*" methods.
  """
  def Echo(self, params):
    return params
  def Square(self, params):
    return {'value': params['value'] * params['value']}
  def Lookup(self, params):
    ret = {}
    values = db.GqlQuery("SELECT * FROM MyData WHERE keyString = '%s'" % params['key'])
    if values.count() > 0:
      ret['value'] = values[0].valueString
      ret['retCode'] = "Ok"
    else:
      ret['retCode'] = "NotFound"
    return ret
  def Store(self, params):
    ret = {}
    email_address = params['username']
    my_email = ops.getCurrentUserEmail()
    values = db.GqlQuery("SELECT * FROM MyData WHERE username = '%s'" % params['username'])
    if values.count() > 0:
      data = values[0]
    else:      
      data = MyData(key_name = email_address)
    
    data.username = ops.getUserNameFromMail(email_address)
    data.department = ops.addUnderscore(params['department'])
    data.submitted = '1'
    data.put()
    ret['retCode'] = "Ok"
    return ret


class RPCHandler(webapp2.RequestHandler):
  """ Allows the functions defined in the RPCMethods class to be RPCed."""

  def __init__(self, request=None, response=None):
     webapp2.RequestHandler.__init__(self, request, response)
     self.methods = RPCMethods()

  def get(self):
    self.post()  # For debugging purposes, you may want this disabled

  def post(self):
    action = self.request.params['action']
    params = self.request.params['params']
    key = self.request.params['key']

    if not key or key != 'mySecretKey':
      self.error(404) # file not found
      return

    if not action:
      self.error(404) # file not found

    if action[0] == '_':
      self.error(403) # access denied
      return

    func = getattr(self.methods, action, None)

    if not func:
      self.error(404) # file not found
      return

    result = func(json.loads(params))
    self.response.out.write(json.dumps(result))

class MyData(db.Model):
  department = db.StringProperty()
  username = db.StringProperty()
  submitted = db.StringProperty()


app = webapp2.WSGIApplication([('/rpc', RPCHandler)],
                              debug=True)

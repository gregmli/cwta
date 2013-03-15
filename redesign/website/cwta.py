import webapp2
from google.appengine.api import users
#from google.appengine.ext import db


import jinja2
import os
import urllib


jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = urllib.quote_plus(s)
    return jinja2.Markup(s)

jinja_environment.filters['urlencode'] = urlencode_filter

class HomePage(webapp2.RequestHandler):
    
    def get(self):
        user = users.get_current_user()

        if user is None:            
            self.redirect(users.create_login_url(self.request.uri))
           
        else:
            template = jinja_environment.get_template('index.html')
            self.response.out.write(template.render(users=users))
            
 


            
            

app = webapp2.WSGIApplication([('/', HomePage)], 
                              debug=True)


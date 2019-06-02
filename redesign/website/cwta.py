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

    
        
class CwtaPage(webapp2.RequestHandler):    
    def get(self, page):        
        template = jinja_environment.get_template(page + '.html')
        self.response.out.write(template.render())
        

class HomePage(CwtaPage):
    def get(self):
        super(HomePage,self).get('index')
        
        

app = webapp2.WSGIApplication([('/', HomePage),
                               ('/(classes|instructors|chen|yang|resources|czl2016)/?(?i)', CwtaPage)
                              ],
                              debug=True)


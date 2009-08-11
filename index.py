
import os
import datetime

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import images
from google.appengine.ext.webapp import template
from google.appengine.api import users

from models import Image
from admin import IMAGE_WIDTH, IMAGE_HEIGHT

class Index(webapp.RequestHandler):
    """
    Main View
    """
    def get(self):
        "Responds to GET requets with the admin interface"
        # query the datastore for images 
        images = Image.all().order("date").fetch(1000)
        context = {
            "images": images,
            "total_width": len(images) * IMAGE_WIDTH
            }
        # calculate the template path
        path = os.path.join(os.path.dirname(__file__), 'templates',
            'index.html')
        # render the template with the provided context
        self.response.out.write(template.render(path, context))


# wire up the views
application = webapp.WSGIApplication([
    ('/', Index)
], debug=True)

def main():
    "Run the application"
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
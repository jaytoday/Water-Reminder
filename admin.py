"""
Provides a protected administrative area for uploading and deleting images
"""

IMAGE_WIDTH = 850
IMAGE_HEIGHT = 450

import os
import datetime

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import images
from google.appengine.ext.webapp import template
from google.appengine.api import users

from models import Image

class Admin(webapp.RequestHandler):
    """
    Admin view for the application.
    Protected to logged in users only.
    """
    def get(self):
        "Responds to GET requets with the admin interface"
        # query the datastore for images
        images = Image.all()
        images.order("date")

        # we are enforcing loggins so we know we have a user
        user = users.get_current_user()
        # we need the logout url for the frontend
        logout = users.create_logout_url("/")

        # prepare the context for the template
        context = {
            "images": images,
            "logout": logout,
            "site_name": "Awkward Beauty"
        }
        # calculate the template path
        path = os.path.join(os.path.dirname(__file__), 'templates',
            'admin.html')
        # render the template with the provided context
        self.response.out.write(template.render(path, context))

class Deleter(webapp.RequestHandler):
    "Deals with deleting images"
    def post(self):
        "Delete a given image"
        # we get the user as you can only delete your own images
        user = users.get_current_user()
        image = db.get(self.request.get("key"))
        # check that we own this image
        if image.user == user:
            image.delete()
        # whatever happens redirect back to the main admin view
        self.redirect('/admin')
       
class Uploader(webapp.RequestHandler):
    "Deals with uploading new images to the datastore"
    def post(self):
        "Upload via a multitype POST message"
        
        try:
            # check we have numerical width and height values
            width = int(self.request.get("width"))
            height = int(self.request.get("height"))
        except ValueError:
            # if we don't have valid width and height values
            # then just use the original image
            image_content = images.resize(self.request.get("img"), 
            IMAGE_WIDTH, IMAGE_HEIGHT)
        else:
            # if we have valid width and height values
            # then resize according to those values
            image_content = images.resize(self.request.get("img"), width, height)
        
        # always generate a thumbnail for use on the admin page
        thumb_content = images.resize(self.request.get("img"), 100, 100)
        
        # create the image object
        image = Image()
        # and set the properties to the relevant values
        image.image = db.Blob(image_content)
        # we always store the original here in case of errors
        # although it's currently not exposed via the frontend
        image.thumb = db.Blob(thumb_content)z
        image.user = users.get_current_user()
        image.title = self.request.get('title')
                
        # store the image in the datasore
        image.put()
        # and redirect back to the admin page
        self.redirect('/admin')
                
# wire up the views
application = webapp.WSGIApplication([
    ('/admin', Admin),
    ('/upload', Uploader),
    ('/delete', Deleter)
], debug=True)

def main():
    "Run the application"
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

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
import google.appengine.api.images
from google.appengine.ext.webapp import template
from google.appengine.api import users

from models import Image

def imageQuery():
  return Image.all().order("date")
  
  
class Admin(webapp.RequestHandler):
    """
    Admin view for the application.
    Protected to logged in users only.
    """
    def get(self):
        "Responds to GET requets with the admin interface"
        # query the datastore for images
        images = imageQuery().fetch(1000)

        # we are enforcing loggins so we know we have a user
        user = users.get_current_user()
        # we need the logout url for the frontend
        logout = users.create_logout_url("/")

        # prepare the context for the template
        context = {
            "images": images,
            "image_count": range(len(images) + 1)[1:],
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
      if self.request.get('img'):
        try:
          # check we have numerical width and height values
          width = int(self.request.get("width"))
          height = int(self.request.get("height"))
        except ValueError:
          # if we don't have valid width and height values
          # then just use the original image
          image_content = google.appengine.api.images.resize(self.request.get("img"), 
          IMAGE_WIDTH, IMAGE_HEIGHT)
          thumb_content = google.appengine.api.images.resize(self.request.get("img"), 100, 100)
        else:
            # if we have valid width and height values
            # then resize according to those values
            image_content = google.appengine.api.images.resize(self.request.get("img"), width, height)
            # always generate a thumbnail for use on the admin page
            thumb_content = google.appengine.api.images.resize(self.request.get("img"), 100, 100)
      else:
        image_content = None
        if not self.request.get('key'):
          logging.critical('No key and no image! Cannot save image.')
          return self.redirect('/admin')

      # check if image is being edited
      if self.request.get('key'):
        image = db.get(self.request.get("key"))
        if self.request.get('position'):
          import datetime
          position = int(self.request.get('position'))
          images = imageQuery().fetch(100)
          offset_image = images.pop(position- 1)
          if position == 1: 
            time_offset = -datetime.timedelta(milliseconds=10)
          else:
            time_offset = datetime.timedelta(milliseconds=10)
          if not offset_image.key() == image.key(): 
            image.date = offset_image.date + time_offset
                
      else:
      # create the image object
        image = Image()
        image.user = users.get_current_user()
      image.title = self.request.get('title')
      if image_content:
      # and set the properties to the relevant values
        image.image = db.Blob(image_content)
        # we always store the original here in case of errors
        # although it's currently not exposed via the frontend
        image.thumb = db.Blob(thumb_content) 
              
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

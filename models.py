from google.appengine.ext import db
from google.appengine.api.users import User

class StickyBitsUser(db.Model):
    "Represents a StickyBits user"
    # stickybits uid
    uid = db.StringProperty()
    phone_number = db.PhoneNumberProperty(required=False)
    date = db.DateTimeProperty(auto_now_add=True)


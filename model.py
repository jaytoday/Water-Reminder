from google.appengine.ext import db
from google.appengine.api.users import User

class Subscriber(db.Model):
    "Represents a Water Reminder Subscriber"
    # key_name - phone_number
    phone_number = db.PhoneNumberProperty(required=False)
    zip_code = db.IntegerProperty(required=False)
    days_subscribed = db.IntegerProperty(required=False)
    call_guid = db.StringProperty() # used to reset scheduled calls
    stickybits_id = db.StringProperty()
    last_scan = db.DateTimeProperty(auto_now_add=True)
    date = db.DateTimeProperty(auto_now_add=True)


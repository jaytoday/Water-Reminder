from google.appengine.ext import db
from google.appengine.api.users import User

class Subscriber(db.Model):
    "Represents a Water Reminder Subscriber"
    # key_name - phone_number
    # TODO: stickybits integration
    stickybits_uid = db.StringProperty()
    days_subscribed = db.IntegerProperty()
    phone_number = db.PhoneNumberProperty(required=False)
    zip_code = db.IntegerProperty(required=False)
    date = db.DateTimeProperty(auto_now_add=True)


import logging
import datetime

import twilio_python.twilio as twilio_api


# Twilio REST API version
API_VERSION = '2008-08-01'

# Twilio AccountSid and AuthToken
ACCOUNT_SID = 'ACd256919c818cae9c4c3cd4498bad7205'
ACCOUNT_TOKEN = '324700e4da46f69f5f218bafb46eb996'
ACCOUNT_NUMBER = '415-483-1286'

SMS_ENDPOINT = 'SMS/Messages'

              

def sendTextMessage(phone_number, message):
  account = twilio_api.Account(ACCOUNT_SID, ACCOUNT_TOKEN)
  arguments = {
    'From' : ACCOUNT_NUMBER,
    'To' : phone_number,
    'Body' : message
    # TODO: 'StatusCallback' post-processing callback
    }
  account.request('/%s/Accounts/%s/%s' % 
                              (API_VERSION, ACCOUNT_SID, SMS_ENDPOINT),
                              'POST', arguments)
  

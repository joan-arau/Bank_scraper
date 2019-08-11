import config
from twilio.rest import Client




account_sid = config.twilio_cred['sid']
auth_token = config.twilio_cred['token']



client = Client(account_sid, auth_token)


def send(msg):
    message = client.messages.create(
                                  body=msg,
                                  from_='+441692252050',
                                  to=str(config.uk_number)
                              )


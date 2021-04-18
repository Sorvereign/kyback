
#remember tjat u delete 6c somewhere on the api key in the json
#remember tjat u delete 6c somewhere on the api key in the json
#remember tjat u delete 6c somewhere on the api key in the json
#remember tjat u delete 6c somewhere on the api key in the json

import imaplib
import email
import os
import re
import hashlib
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from email.header import decode_header

import threading

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("kyiuba-firebase-adminsdk-sy056-6c4347a44a.json")
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL': "https://kyiuba-default-rtdb.firebaseio.com/"
	})

ref = db.reference("/")
result = ref.get()

# account credentials

username = os.environ['em_email']

password = os.environ['em_password']



def get_email(string):
    match = re.search("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",
                       string)
    return match.group(1)

def start():
    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    imap.login(username, password)

    (status, messages) = imap.select('INBOX')

    threading.Timer(5.0, start).start()
    #ex every 5 secs
    # number of top emails to fetch

    N = 100 

    # push key
    emails = []

    # total number of emails

    messages = int(messages[0])
    for i in range(messages, messages - N, -1):

    # fetch the email message by ID

        res, msg = imap.fetch(str(i), '(RFC822)')
        for response in msg:
            if isinstance(response, tuple):

            # parse a bytes email into a message object

                msg = email.message_from_bytes(response[1])

            # decode the email subject

            #    (subject, encoding) = decode_header(msg['Subject'])[0]
            #    if isinstance(subject, bytes):

            #        subject = subject.decode(encoding)

                From, encoding = decode_header(msg.get('From'))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                #if 'almer_d@hotmail.com' in From:
                #    print ('epa 2', subject)

            # if the email message is multipart

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = \
                            str(part.get('Content-Disposition'))
                        if content_type == 'text/plain' \
                            and 'attachment' not in content_disposition \
                            and 'almer_d@hotmail.com' in From:
                            body = part.get_payload(decode=True)  # decode
                            body2 = str(body.decode('latin-1'))
                            ref.push().set(get_email(body2))
                            try:
                              client = MailchimpMarketing.Client()
                              client.set_config({
                                  "api_key": os.environ['chimp_key'],
                                 "server": "us1"
                              })
                              response = client.lists.add_list_member(os.environ['list_id'], {"email_address": get_email(body2), "status": "subscribed"})
                              #response2 = response = client.lists.get_list_member_tags(os.environ["list_id"], "testasdahyt12213@fhy22.com")
                              response2 = client.lists.batch_segment_members({"members_to_add": [get_email(body2)]}, os.environ['list_id'], "3092922")
                              print(response2)
                            except ApiClientError as error:
                               print(error.text)
                            break

    imap.close()
    imap.logout()
start()


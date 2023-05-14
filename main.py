"""
Copyright (c) 2023, Charles HL. All rights reserved.
"""
import os
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
import google_auth_oauthlib.flow
import re
import email.utils as email_utils
import email.message as email_message_lib
import time

TIME_BETWEEN_EMAILS_IN_S = 4 # in seconds

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email) or email_utils.parseaddr(email)[1]:
        return True
    else:
        return False

def create_message(sender, to, subject, message_text):
    message = email_message_lib.EmailMessage()
    message['From'] = sender
    message['To'] = to
    message['Subject'] = subject
    message.set_content(message_text, subtype='plain', charset='utf-8')
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')}

def send_message(message):
    try:
        service.users().messages().send(userId='me', body=message).execute()
        print("Email sent successfully.")
    except HttpError as error:
        print(f"An error occurred while sending the email: {error}")

def send_emails(sender, recipients, subject, message_text):
    for recipient in recipients:
        message = create_message(sender, recipient, subject, message_text)
        print(f"Sending email to {recipient}...")
        send_message(message)
        if recipient != recipients[-1]:
            print(f"Waiting {TIME_BETWEEN_EMAILS_IN_S} seconds before sending the next email...")
            time.sleep(TIME_BETWEEN_EMAILS_IN_S)

if __name__ == '__main__':

    print("-----------------------------")
    print("Script to send one email to multiple email addresses with Gmail API")
    print("-----------------------------")

    print("\nChecking credentials for Gmail API...")
    # Set up credentials
    credentials = None
    if os.path.exists('config/token.json'):
        credentials = Credentials.from_authorized_user_file('config/token.json')
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                'config/credentials.json', ['https://www.googleapis.com/auth/gmail.send'])
            credentials = flow.run_local_server(port=0)
        with open('config/token.json', 'w') as token:
            token.write(credentials.to_json())

    # Create a Gmail API service
    service = build('gmail', 'v1', credentials=credentials)
    
    # Read email address of the sender from a text file
    with open('email-info/email_sender.txt', 'r') as file:
        sender_email = file.read()
    # Check if the sender email is valid
    if not is_valid_email(sender_email):
        raise Exception(f"Invalid email: {sender_email}")
    # Check if the file only contains one email address
    if '\n' in sender_email or '\r' in sender_email:
        raise Exception("Sender email contains line breaks.")    

    print("Sender email: " + sender_email)

    print("Checking email recipients, subject and message...")

    # Read recipient emails from a text file where each line is an email address
    with open('email-info/email_recipients.txt', 'r') as file:
        recipient_emails = file.readlines()
    recipient_emails = [email.strip() for email in recipient_emails]
    # Check if there is at least one recipient
    if not recipient_emails:
        raise Exception("No recipient emails provided.")
    # Check if all emails are valid
    for email in recipient_emails:
        if not is_valid_email(email):
            raise Exception(f"Invalid email: {email}")
    # Remove duplicate emails
    recipient_emails = list(set(recipient_emails))

    # Read email subject from a text file and check its length and validity
    with open('email-info/email_subject.txt', 'r') as file:
        email_subject = file.read()
    if len(email_subject) > 78:
        raise Exception("Subject length exceeds 78 characters.")
    if not email_subject:
        raise Exception("Subject is empty.")
    # Verify that the subject does not contain any line breaks
    if '\n' in email_subject or '\r' in email_subject:
        raise Exception("Subject contains line breaks.")

    # Read email message from a text file
    with open('email-info/email_message.txt', 'r') as file:
        email_message = file.read()
    # Check if the message is empty
    if not email_message:
        raise Exception("Message is empty.")

    print("Emails ready to be sent.\n")
    send_emails(sender_email, recipient_emails, email_subject, email_message)

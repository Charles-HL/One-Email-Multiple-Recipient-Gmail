# One Email Multiple Recipient with Gmail

This script allows you to send a single email to multiple recipients using the Gmail API. It reads the necessary information from text files and verifies the validity of the email addresses and content before sending the email.

## Prerequisites
Before using this script, make sure you have the following:
- Google API credentials: You need to have a `credentials.json` file obtained by creating a project in the Google Developers Console and enabling the Gmail API. Place this file in the config directory. You can follow this guide to help you : [developers.google.com/gmail/api/quickstart/python](https://developers.google.com/gmail/api/quickstart/python)
- Token file: A token.json file will be generated after authenticating the script with your Google account. If the file does not exist, it will be created automatically.
- Text files with email information: The script reads the sender's email address, recipient email addresses, subject, and message from separate text files located in the email-info directory.

## Installation
1. Clone the repository and navigate to the project directory.
2. Install the required dependencies by running the following command:
```
pip install requirements.txt
```
3. Ensure the following directory structure:
```
project/
├── config/
│   ├── credentials.json
└── email-info/
    ├── email_sender.txt
    ├── email_recipients.txt
    ├── email_subject.txt
    └── email_message.txt
```

4. Replace the content of email_sender.txt with the sender's email address.

5. Add recipient email addresses, one per line, in the `email_recipients.txt` file.

6. Customize the email subject in the `email_subject.txt` file.

7. Write the email message in the `email_message.txt` file.

## Usage
Run the script using the following command:
```
python main.py
```
The script will perform the following steps:

- Check the credentials for the Gmail API and authenticate if necessary.

- Read the sender's email address from email_sender.txt and validate its format.

- Read the recipient email addresses from email_recipients.txt, validate their formats, and ensure there is at least one recipient.

- Read the email subject from email_subject.txt, check its length (must not exceed 78 characters), and ensure it is not empty.

- Read the email message from email_message.txt and ensure it is not empty.

- Send the email to each recipient sequentially, with a delay of TIME_BETWEEN_EMAILS_IN_S seconds between each email.

The script will output status messages to the console, indicating the progress of the email sending process.

Note: The script assumes that the Gmail API is enabled and the necessary permissions are granted to the credentials associated with the credentials.json file.


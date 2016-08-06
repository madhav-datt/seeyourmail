#
# A wrapper around the imaplib Python Package
# Retrieve emails from @gmail.com addresses
#
# Copyright (C)   2016    Madhav Datt
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
#

import imaplib
import os
import email
from authenticate import connect_email_account, get_password

# Email login credentials
_username = None

# Connecting to the gmail IMAP server
imap_conn = imaplib.IMAP4_SSL("imap.gmail.com")


def login(username, password=None):
    """
    Login to email account from which emails have to be retrieved

    :param username: email address for gmail account to be used
    :param password: password for gmail account associated with username
    """
    global _username
    _username = username

    if password:
        connect_email_account(username, password)

    imap_conn.login(_username, get_password(_username))

    # Select gmail mail box to retrieve emails from
    imap_conn.select("[Gmail]/All Mail")


def getmail():
    """

    :return: list of emails retrieved according to selected parameters
    """

    # Filter emails based on IMAP rules
    response, items = imap_conn.search(None, "ALL")
    mail_items = items[0].split()

    for email_id in mail_items:
        # Fetch and parse entire email's contents
        response, data = imap_conn.fetch(email_id, "(RFC822)")
        email_body = data[0][1]
        mail = email.message_from_string(email_body)

        # Email contents and data dictionary
        _mail_dict = {
            'from': mail['from'],
            'to': mail['to'],
            'date': mail['date'],
            'subject': mail['subject'],
            'from'
        }
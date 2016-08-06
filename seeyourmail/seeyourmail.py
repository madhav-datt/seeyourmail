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
    # TODO validate email id as gmail, error handling
    if password:
        connect_email_account(username, password)

    imap_conn.login(_username, get_password(_username))

    # Select gmail mail box to retrieve emails from
    imap_conn.select("[Gmail]/All Mail")


def getmail():
    """

    :return: list of emails retrieved according to selected parameters
    """

    mail_list = []

    # Filter emails based on IMAP rules
    response, items = imap_conn.search(None, "ALL")
    mail_items = items[0].split()

    for email_id in mail_items:
        # Fetch and parse entire email's contents
        response, data = imap_conn.fetch(email_id, "(RFC822)")
        email_body = data[0][1]
        mail = email.message_from_string(email_body)

        # Parse sender's name from the email object's from field
        sender = mail['from'].split()[:-1]
        sender = ' '.join(sender)[1:-1]

        attachment = None
        content = ''

        if mail.is_multipart():
            for part in mail.walk():

                # Skip containers/multipart objects
                if part.is_multipart():
                    continue

                # is this part an attachment ?
                if part.get('Content-Disposition') is None:
                    continue

                filename = part.get_filename()
                counter = 1

                # if there is no filename, we create one with a counter to avoid duplicates
                if not filename:
                    filename = 'part-%03d%s' % (counter, 'bin')
                    counter += 1

                att_path = os.path.join(detach_dir, filename)

                # Check if its already there
                if not os.path.isfile(att_path):
                    # finally write the stuff
                    fp = open(att_path, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()

        else:
            content = mail.get_payload()

        # Email contents and data dictionary
        _mail_dict = {
            'from': mail['return-path'],
            'to': mail['to'],
            'date': mail['date'],
            'subject': mail['subject'],
            'sender': sender,
            'content': content,
            'attachment': attachment,
            'email': mail
        }
        mail_list.append(_mail_dict)

    return mail_list

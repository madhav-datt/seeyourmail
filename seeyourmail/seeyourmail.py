#
# A wrapper around the imaplib Python Package
# Retrieve emails from @gmail.com addresses
#
# Copyright (C)   2016    Madhav Datt
# https://opensource.org/licenses/MIT
#

import imaplib
import email
import io
from os import mkdir
from os.path import isfile, join, isdir

# Hacky import error fix for interactive loading
try:
    from .authenticate import connect_email_account, get_password
    from .errors import AuthenticationError, SearchCriteriaError
    from .validate import validate_email
    from .nlp_process import nlp_process

except (ValueError, SystemError, ImportError):
    from authenticate import connect_email_account, get_password
    from errors import AuthenticationError, SearchCriteriaError
    from validate import validate_email
    from nlp_process import nlp_process


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
    validate_email(username)

    if password:
        connect_email_account(username, password)


def getmail(search_condition=None, dir_path='~/sym_data'):
    """
    Fetch, parse and arrange email contents from specified mail account according to inputted
    natural language search criteria
    :param search_condition: natural language english input with email search criteria
    :param dir_path: path where email attachments are downloaded and stored
    :return: list of emails retrieved according to selected parameters
    :raises AuthenticationError: if login fails/could not authenticate
    :raises SearchCriteriaError: if search criteria could not be built from natural language input
    """

    mail_box, search_criteria = nlp_process(search_condition)

    response, _ = imap_conn.login(_username, get_password(_username))
    if response != 'OK':
        raise AuthenticationError('Login Failed')

    # Select gmail mail box to retrieve emails from
    imap_conn.select(mail_box)

    mail_list = []

    if not isdir(dir_path):
        mkdir(dir_path)

    # Filter emails based on IMAP rules
    response, items = imap_conn.search(None, search_criteria)
    if response != 'OK':
        raise SearchCriteriaError('Search criteria building failed. Could not parse conditions')

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
        counter = 1

        if mail.is_multipart():

            # Directory to store attachments associated with multipart email
            email_dir_path = join(dir_path, '{email_num}_{subject}'.format(email_num=email_id,
                                                                           subject=mail['subject'][:5]))
            mkdir(email_dir_path)

            for part in mail.walk():

                # Skip containers/multipart objects
                if part.is_multipart():
                    continue

                # If part is text/not an attachment
                if part.get('Content-Disposition') is None:
                    content_type = part.get_content_type()
                    if content_type == 'text/plain' or content_type == 'text/html':
                        # Retrieve body text/contents of email as plain text
                        content = content + '' + part.get_payload()
                    continue

                # Download and save files attached to email
                filename = part.get_filename()

                # If no filename, create filename using a counter to avoid duplicates
                if not filename:
                    filename = "file_{count}".format(count=counter)
                    counter += 1

                attach_dir_path = join(email_dir_path, filename)

                # Check if file already exists
                if not isfile(attach_dir_path):
                    with io.open(attach_dir_path, 'wb') as attach_file_path:
                        attach_file_path.write(part.get_payload(decode=True))
                        attach_file_path.close()

        else:
            content = mail.get_payload()

        # Email contents and data dictionary
        mail_dict = {
            'from': mail['return-path'],
            'to': mail['to'],
            'date': mail['date'],
            'subject': mail['subject'],
            'sender': sender,
            'content': content,
            'attachment': attachment,
            'email': mail
        }
        mail_list.append(mail_dict)

    return mail_list

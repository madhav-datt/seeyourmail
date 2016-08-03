#
# SendMail Class - a wrapper around the SMTP Python Package
# Send emails from @gmail.com addresses
#
# Copyright (C)   2016    Madhav Datt
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
#

import poplib
from email import parser
from authenticate import connect_email_account, get_password

# Email login credentials
_username = None
pop_conn = poplib.POP3_SSL('pop.gmail.com')


def login(username, password=None):
    """
    Login to email account from which emails have to be retrieved

    :param username: email address for gmail account to be used
    :param password: password for gmail account associated with username
    :return:
    """
    global _username
    _username = username

    if password:
        connect_email_account(username, password)

    pop_conn.user(_username)
    pop_conn.pass_(get_password(_username))


# Get messages from server:
messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]

# Concat message pieces:
messages = ["\n".join(message[1]) for message in messages]

# Parse message intom an email object:
messages = [parser.Parser().parsestr(message) for message in messages]

pop_conn.quit()

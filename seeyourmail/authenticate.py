#
# Store and use login credentials with keyring for seeyourmail
#
# Copyright (C)   2016    Madhav Datt
# https://opensource.org/licenses/MIT
#

import getpass
import keyring
import keyring.errors


def connect_email_account(email, password):
    """
    Securely store password in Python keyring
    :param email: Email address for account to be used with clmail
    :param password: Password for email address
    :raises keyring.errors.PasswordSetError
    """

    # Raises keyring.errors.PasswordSetError if password not set
    keyring.set_password('symail', email, password)


def get_password(email):
    """
    :param email: Email address for account associated with clmail
    :return: Password for email address
    """

    # None if password doesn't exist
    password = keyring.get_password('symail', email)

    if password is None:
        password = getpass.getpass("Password for {email_id}: ".format(email_id=email))
        connect_email_account(email, password)

    return password


def remove_email(email):
    """
    Remove stored email and password from keyring
    :param email: Email address for account associated with clmail
    """

    try:
        keyring.delete_password('symail', email)
    except keyring.errors.PasswordDeleteError:
        pass

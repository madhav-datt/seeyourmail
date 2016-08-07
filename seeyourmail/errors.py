#
# Contains custom exceptions raised by the program
#
# Copyright (C)   2016    Madhav Datt
# https://opensource.org/licenses/MIT
#


class SearchCriteriaError(Exception):
    """
    The natural language criteria for email filtration could not be parsed/understood and converted to a structured
    search query. There may be contradicting/conflicting/incomplete/unclear search criteria.
    """

    pass


class EmailAddressError(Exception):
    """
    Email address was either invalid or not a gmail address. Note that this only filters out syntactical mistakes in
    email address, so all "valid looking" email address get accepted as such.
    """

    pass


class AuthenticationError(Exception):
    """
    Authentication failed. Either due an incorrect password, or if gmail two-step authentication is activated, or if
    less secure apps are not allowed to access the specified gmail account. To enable access from less secure apps,
    follow the steps at https://support.google.com/mail/answer/78754
    """

    pass

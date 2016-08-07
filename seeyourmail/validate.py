#
# RFC 2822 - style email validation for Python
# (c) 2012 Syrus Akbary <me@syrusakbary.com>
# Extended from (c) 2011 Noel Bush <noel@aitools.org>
# for support of mx and user check
# This code is made available to you under the GNU LGPL v3.
#
# This module provides a single method, valid_email_address(),
# which returns True or False to indicate whether a given address
# is valid according to the 'addr-spec' part of the specification
# given in RFC 2822.  Ideally, we would like to find this
# in some other library, already thoroughly tested and well-
# maintained.  The standard Python library email.utils
# contains a parse_addr() function, but it is not sufficient
# to detect many malformed addresses.
#
# This implementation aims to be faithful to the RFC, with the
# exception of a circular definition (see comments below), and
# with the omission of the pattern components marked as "obsolete".
#

import re
from errors import EmailAddressError

#
# All we are really doing is comparing the input string to one
# gigantic regular expression.  But building that regexp, and
# ensuring its correctness, is made much easier by assembling it
# from the "tokens" defined by the RFC.  Each of these tokens is
# tested in the accompanying unit test file.
#
# The section of RFC 2822 from which each pattern component is
# derived is given in an accompanying comment.
#
# (To make things simple, every string below is given as 'raw',
# even when it's not strictly necessary.  This way we don't forget
# when it is necessary.)
#

# See 2.2.2. Structured Header Field Bodies
WSP = r'[ \t]'

# See 2.2.3. Long Header Fields
CRLF = r'(?:\r\n)'

# See 3.2.1. Primitive Tokens
NO_WS_CTL = r'\x01-\x08\x0b\x0c\x0f-\x1f\x7f'

# See 3.2.2. Quoted characters
QUOTED_PAIR = r'(?:\\.)'
FWS = r'(?:(?:' + WSP + r'*' + CRLF + r')?' + WSP + r'+)'

# See 3.2.3. Folding white space and comments
CTEXT = r'[' + NO_WS_CTL + r'\x21-\x27\x2a-\x5b\x5d-\x7e]'
CCONTENT = r'(?:' + CTEXT + r'|' + QUOTED_PAIR + r')'
COMMENT = r'\((?:' + FWS + r'?' + CCONTENT + r')*' + FWS + r'?\)'
CFWS = r'(?:' + FWS + r'?' + COMMENT + ')*(?:' + FWS + '?' + COMMENT + '|' + FWS + ')'

# See 3.2.4 Atom
ATEXT = r'[\w!#$%&\'\*\+\-/=\?\^`\{\|\}~]'
ATOM = CFWS + r'?' + ATEXT + r'+' + CFWS + r'?'
DOT_ATOM_TEXT = ATEXT + r'+(?:\.' + ATEXT + r'+)*'
DOT_ATOM = CFWS + r'?' + DOT_ATOM_TEXT + CFWS + r'?'

# See 3.2.5. Quoted strings
QTEXT = r'[' + NO_WS_CTL + r'\x21\x23-\x5b\x5d-\x7e]'
QCONTENT = r'(?:' + QTEXT + r'|' + QUOTED_PAIR + r')'
QUOTED_STRING = CFWS + r'?' + r'"(?:' + FWS + r'?' + QCONTENT + r')*' + FWS + r'?' + r'"' + CFWS + r'?'

# See 3.4.1. Address-spec specification
LOCAL_PART = r'(?:' + DOT_ATOM + r'|' + QUOTED_STRING + r')'

DTEXT = r'[' + NO_WS_CTL + r'\x21-\x5a\x5e-\x7e]'
DCONTENT = r'(?:' + DTEXT + r'|' + QUOTED_PAIR + r')'
DOMAIN_LITERAL = CFWS + r'?' + r'\[' + r'(?:' + FWS + r'?' + DCONTENT + r')*' + FWS + r'?\]' + CFWS + r'?'
DOMAIN = r'(?:' + DOT_ATOM + r'|' + DOMAIN_LITERAL + r')'

ADDRESS_SPEC = LOCAL_PART + r'@' + DOMAIN

# Valid email address will match exactly the 3.4.1 address-spec.
VALID_ADDRESS_REGEXP = '^' + ADDRESS_SPEC + '$'

# Exactly match gmail email addresses
GMAIL_REGEXP = '^' + LOCAL_PART + r'@' + 'gmail.com' + '$'


def validate_email(email):
    """
    Will only filter out syntax mistakes in email addresses
    Most "valid looking" gmail email address will pass even if the email address is not
    claimed or used by a user
    :raises EmailAddressError
    """

    if not re.match(GMAIL_REGEXP, email):
        raise EmailAddressError('Invalid gmail address')

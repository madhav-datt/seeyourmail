#
# SendMail Class - a wrapper around the SMTP Python Package
# Send emails from @gmail.com addresses
#
# Copyright (C)   2016    Madhav Datt
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
#

import poplib
from email import parser

pop_conn = poplib.POP3_SSL('pop.gmail.com')
pop_conn.user(username)
pop_conn.pass_(password)

# Get messages from server:
messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]

# Concat message pieces:
messages = ["\n".join(message[1]) for message in messages]

# Parse message intom an email object:
messages = [parser.Parser().parsestr(message) for message in messages]

pop_conn.quit()

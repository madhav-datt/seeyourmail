#
# Contains natural language processing and search criteria generation functions
#
# Copyright (C)   2016    Madhav Datt
# https://opensource.org/licenses/MIT
#

import nltk
stemmer = nltk.snowball.EnglishStemmer()
# TODO improve criteria generation with ML based stop-word, keyword lists


def nlp_process(search_cond):
    """
    Build structured search criteria from constraints specified in the natural language input string
    :param search_cond: natural language english input with email search criteria
    :return: mail_box, gmail mail box to retrieve emails from
    :return: search_criteria, structured search criteria string
    """

    if search_cond is None:
        return '[Gmail]/All Mail', 'ALL'

    mail_box_list = ['INBOX', '[Gmail]', '[Gmail]/All Mail', '[Gmail]/Drafts', '[Gmail]/Important', '[Gmail]/Sent Mail',
                     '[Gmail]/Spam', '[Gmail]/Starred', '[Gmail]/Trash']

    mail_type = ['ANSWERED', 'UNANSWERED', 'ALL', 'SEEN', 'UNSEEN', 'RECENT', 'OLD', 'NEW', 'DELETED']

    mail_date = {'on': 'SENTON {date}', 'after': 'SENTSINCE {date}', 'before': 'SENTBEFORE {date}'}

    mail_field = {'from': 'FROM "{search_text}"', 'to': 'TO "{search_text}"', 'subject': 'SUBJECT "{search_text}"',
                  'body': 'BODY "{search_text}"', 'text': 'TEXT "{search_text}"'}

    mail_size = {'small': 'SMALLER {size}', 'large': 'LARGER {size}'}

    or_key = 'OR'
    and_key = 'AND'


def _nlp_process(search_cond):
    """
    Build structured search criteria from constraints specified in the natural language input string
    :param search_cond: natural language english input with email search criteria
    :return: mail_box, gmail mail box to retrieve emails from
    :return: search_criteria, structured search criteria string
    """

    mail_box_list = ['INBOX', '[Gmail]', '[Gmail]/All Mail', '[Gmail]/Drafts', '[Gmail]/Important', '[Gmail]/Sent Mail',
                     '[Gmail]/Spam', '[Gmail]/Starred', '[Gmail]/Trash']

    mail_type = ['ANSWERED', 'UNANSWERED', 'ALL', 'SEEN', 'UNSEEN', 'RECENT', 'OLD', 'NEW', 'DELETED']

    mail_date = ['SENTON {date}', 'SENTSINCE {date}', 'SENTBEFORE {date}']

    mail_field = ['FROM "{search_text}"', 'TO "{search_text}"', 'SUBJECT "{search_text}"', 'BODY "{search_text}"',
                  'TEXT "{search_text}"']

    mail_size = ['SMALLER {size}', 'LARGER {size}']

    if search_cond is None:
        return '[Gmail]/All Mail', 'ALL'

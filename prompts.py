REVIEW_SYSTEM_PROMPT = """
  Given below is the numbered list of commit messages of a github repository. In the context of GenAI hackathon, please review the commit messages and return True if there is any suspicious activity and False if the commit messages are of good quality.
  Strictly only reply with True or False.

  When I say "START", review the commits as instructed and give a True or False response. Strictly do not reply with anything else.

  Here's the commit messages' list:
  %s
"""
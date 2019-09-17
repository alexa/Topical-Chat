# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT
import praw
from prawcore.exceptions import ServerError

class Prawler:

    def __init__(self, reddit_client_id, reddit_client_secret, reddit_client_user_agent):
        self._CLIENT_ID = reddit_client_id
        self._CLIENT_SECRET = reddit_client_secret
        self._USER_AGENT = reddit_client_user_agent
        self._TIL_THAT = "til that"
        self._TIL_ABOUT = "til about"
        self._TIL_OF = "til of"
        self._TODAY_I_LEARNED_THAT = "today i learned that"
        self._TODAY_I_LEARNED_ABOUT = "today i learned about"
        self._TODAY_I_LEARNED_OF = "today i learned of"
        self._TIL = "til"
        self._TODAY_I_LEARNED = "today i learned"
        self._reddit = praw.Reddit(client_id=self._CLIENT_ID, client_secret=self._CLIENT_SECRET,
                                   user_agent=self._USER_AGENT)
        self._retries = 3

    def get(self, fullname):
        retries = self._retries
        id = fullname[3:]
        while retries > 0:
            try:
                submission = self._reddit.submission(id=id)
                break
            except ServerError as e:
                if retries == 0:
                    raise e
                retries = retries - 1
        return self.clean(submission.title)

    def clean(self, text):
        start_idx = 0

        if text.lower().startswith(self._TIL_THAT):
            start_idx = len(self._TIL_THAT) + 1
        elif text.lower().startswith(self._TIL_ABOUT):
            start_idx = len(self._TIL_ABOUT) + 1
        elif text.lower().startswith(self._TIL_OF):
            start_idx = len(self._TIL_OF) + 1
        elif text.lower().startswith(self._TODAY_I_LEARNED_THAT):
            start_idx = len(self._TODAY_I_LEARNED_THAT) + 1
        elif text.lower().startswith(self._TODAY_I_LEARNED_ABOUT):
            start_idx = len(self._TODAY_I_LEARNED_ABOUT) + 1
        elif text.lower().startswith(self._TODAY_I_LEARNED_OF):
            start_idx = len(self._TODAY_I_LEARNED_OF) + 1
        elif text.lower().startswith(self._TIL):
            start_idx = len(self._TIL) + 1
        elif text.lower().startswith(self._TODAY_I_LEARNED):
            start_idx = len(self._TODAY_I_LEARNED) + 1
        text = text[start_idx:].strip()

        return text


if __name__ == '__main__':
    prawler = Prawler()
    thread_id = "t3_191mj0"
    title = prawler.get(thread_id)
    print(title)

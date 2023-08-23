# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT

import praw
import time
from functools import lru_cache


class Prawler:

    def __init__(self, name):
        # TODO: replace with your own credentials and made-up user agent
        self._CLIENT_ID = ""
        self._CLIENT_SECRET = ""
        self._USER_AGENT = ""

        if not self._CLIENT_ID or not self._CLIENT_SECRET or not self._USER_AGENT:
            raise ValueError("Reddit credentials are empty!\nPlease manually add your client ID, client secret and "
                             "a made-up user agent to /src/reddit/prawler.py\n"
                             "You can obtain your client ID and client secret by signing up for Reddit credentials "
                             "here: https://www.reddit.com/wiki/api")

        self._reddit = praw.Reddit(client_id=self._CLIENT_ID, client_secret=self._CLIENT_SECRET,
                                   user_agent=self._USER_AGENT)
        self._subreddit = self._reddit.subreddit(name)

        # memoization to prevent excess calls to Reddit
        self.prawl = lru_cache(maxsize=None)(self.get)

    def get(self, fullname):
        """
        This API provides the ability to fetch the cleaned title of a Reddit submission, given its thread id
        """

        if fullname[0:3] != "t3_":
            raise ValueError("Passed fullname must reference a Reddit submission (i.e., begin with 't3_')!")
        id = fullname[3:]  # ignore the data type since we know it's intended to be a submission

        submission = self._reddit.submission(id=id)
        return self.clean(submission.title)


class TodayILearnedPrawler(Prawler):
    def __init__(self):
        super().__init__(name='todayilearned')

        self._TIL_THAT = "til that"
        self._TIL_ABOUT = "til about"
        self._TIL_OF = "til of"
        self._TODAY_I_LEARNED_THAT = "today i learned that"
        self._TODAY_I_LEARNED_ABOUT = "today i learned about"
        self._TODAY_I_LEARNED_OF = "today i learned of"
        self._TIL = "til"
        self._TODAY_I_LEARNED = "today i learned"

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


if __name__ == "__main__":
    prawler = TodayILearnedPrawler()

    start_time = time.time()
    for idx in range(10):
        fullname = "t3_162ifa"
        title = prawler.get(fullname)
    print(title)
    end_time = time.time()
    duration = (end_time - start_time) * 1000

    print("Duration before caching:", duration, "ms")

    start_time = time.time()
    for idx in range(10):
        fullname = "t3_162ifa"
        title = prawler.prawl(fullname)
    print(title)
    end_time = time.time()
    duration = (end_time - start_time) * 1000

    print("Duration after caching:", duration, "ms")

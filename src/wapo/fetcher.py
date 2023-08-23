# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT

import requests
from functools import lru_cache
import time


class WaPoFetcher:
    def __init__(self):
        self._TOPICAL_CHAT_WAPO_API_ENDPOINT = "https://0tevsac2i8.execute-api.us-east-1.amazonaws.com/prod"
        self._API_KEY = "nMEYN1wagz89BLpgcmi1m1yg5d5qMCucaBIgNyU1"

        # memoization to prevent excess calls to the API endpoint
        self.fetch = lru_cache(maxsize=None)(self.fetch_wapo_article_sections)

    def fetch_wapo_article_sections(self, article_url):
        response = requests.get(self._TOPICAL_CHAT_WAPO_API_ENDPOINT,
                                headers={'Accept': 'application/json'},
                                params={'article_url': article_url, 'x-api-key': self._API_KEY})
        return response.json()


if __name__ == "__main__":

    fetcher = WaPoFetcher()

    article_url = "http://www.washingtonpost.com/politics/2018/11/20/candidate-photographed-confederate-garb-could-be-scandal-will-it-be-mississippi/"

    start_time = time.time()
    for idx in range(10):
        article_sections = fetcher.fetch_wapo_article_sections(article_url)
    end_time = time.time()
    duration = (end_time - start_time) * 1000

    print("Duration before caching:", duration, "ms")

    start_time = time.time()
    for idx in range(10):
        article_sections = fetcher.fetch(article_url)
    end_time = time.time()
    duration = (end_time - start_time) * 1000

    print("Duration after caching:", duration, "ms")

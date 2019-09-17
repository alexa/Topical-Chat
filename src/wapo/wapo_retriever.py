# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT
import requests


class WapoRetriever:
    def __init__(self):
        self._TOPICAL_CONTENT_WAPO_API_HTTP_ENDPOINT = \
            'https://0tevsac2i8.execute-api.us-east-1.amazonaws.com/prod'
        self._API_KEY = 'nMEYN1wagz89BLpgcmi1m1yg5d5qMCucaBIgNyU1'
        self._retries = 3

    def get_wapo_article_section(self, article_url):
        retries = self._retries
        while retries > 0:
            try:
                response = requests.get(self._TOPICAL_CONTENT_WAPO_API_HTTP_ENDPOINT,
                                headers = {'Accept': 'application/json'}, params={'article_url': article_url,
                                                                                  'x-api-key': self._API_KEY})
                return response.json()

            except Exception as e:
                if retries == 0:
                    raise e
                retries = retries - 1

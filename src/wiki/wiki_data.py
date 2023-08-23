# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT

import json


class WikiData:
    def __init__(self):
        self._id_to_shortened_wiki_lead_section = dict()
        self._id_to_summarized_wiki_lead_section = dict()
        self._load_data()

    def _load_data(self):
        with open("wiki/wiki.json", "r") as f:
            _wiki_data = json.load(f)
            shortened_wiki_lead_section = _wiki_data["shortened_wiki_lead_section"]
            summarized_wiki_lead_section = _wiki_data["summarized_wiki_lead_section"]

            for key in shortened_wiki_lead_section.keys():
                value = shortened_wiki_lead_section[key]
                self._id_to_shortened_wiki_lead_section[value] = key

            for key in summarized_wiki_lead_section.keys():
                value = summarized_wiki_lead_section[key]
                self._id_to_summarized_wiki_lead_section[value] = key

    def get_wiki_text(self, key, id):
        if key == "shortened_wiki_lead_section":
            return self._id_to_shortened_wiki_lead_section[id]
        elif key == "summarized_wiki_lead_section":
            return self._id_to_summarized_wiki_lead_section[id]

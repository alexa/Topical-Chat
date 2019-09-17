# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT

import json


class WikiData:
    def __init__(self):
        self.id_to_shortened_wiki_lead_section_mapping = {}
        self.id_to_summarized_wiki_lead_section = {}
        self.load_data()

    def load_data(self):
        with open("wiki/wiki.json", "r") as f:
            wiki_data = json.load(f)
            shortened_wiki_lead_section = wiki_data['shortened_wiki_lead_section']
            summarized_wiki_lead_section = wiki_data['summarized_wiki_lead_section']

            for key in shortened_wiki_lead_section.keys():
                value = shortened_wiki_lead_section[key]
                self.id_to_shortened_wiki_lead_section_mapping[value] = key

            for key in summarized_wiki_lead_section.keys():
                value = summarized_wiki_lead_section[key]
                self.id_to_summarized_wiki_lead_section[value] = key

    def get_wiki_text(self, key, wiki_id):
        if key == 'shortened_wiki_lead_section':
            return self.id_to_shortened_wiki_lead_section_mapping[wiki_id]
        elif key == 'summarized_wiki_lead_section':
            return self.id_to_summarized_wiki_lead_section[wiki_id]

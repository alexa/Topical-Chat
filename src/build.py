# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT

import json
import os
import hashlib
from tqdm import tqdm
from reddit.prawler import TodayILearnedPrawler
from wapo.fetcher import WaPoFetcher
from wiki.wiki_data import WikiData


class TopicalChatBuilder:
    def __init__(self):
        self._pre_build_dir = "../reading_sets/pre-build/"
        self._post_build_dir = "../reading_sets/post-build/"
        self._post_build_hashes = "../reading_sets/file_hashes.json"
        self._wikidata = WikiData()
        self._prawler = TodayILearnedPrawler()
        self._fetcher = WaPoFetcher()
        self._agents = ["agent_1", "agent_2"]

    def _get_article_section(self, article_url):
        if article_url is not None:
            # Fetch WaPo article by making API call to Amazon endpoint
            wapo_article = self._fetcher.fetch(article_url)
            wapo_article["url"] = article_url
        else:
            print("article_url is None! Something went wrong!")
            wapo_article = dict()
        return wapo_article

    def _populate_factual_section(self, reading_sets, conversation_id, agent):

        factual_section_keys = reading_sets[conversation_id][agent].keys()
        for key in factual_section_keys:
            thread_ids = reading_sets[conversation_id][agent][key]["fun_facts"]
            fun_facts = []
            # Fetch fun facts by making Reddit API call with thread ID
            for thread_id in thread_ids:
                fun_fact = self._prawler.prawl(thread_id)
                fun_facts.append(fun_fact)

            reading_sets[conversation_id][agent][key]["fun_facts"] = fun_facts

            if "shortened_wiki_lead_section" in reading_sets[conversation_id][agent][key]:
                wiki_id = reading_sets[conversation_id][agent][key]["shortened_wiki_lead_section"]
                reading_sets[conversation_id][agent][key]["shortened_wiki_lead_section"] =\
                    self._wikidata.get_wiki_text("shortened_wiki_lead_section", wiki_id)
            elif "summarized_wiki_lead_section" in reading_sets[conversation_id][agent][key]:
                wiki_id = reading_sets[conversation_id][agent][key]["summarized_wiki_lead_section"]
                reading_sets[conversation_id][agent][key]["summarized_wiki_lead_section"] =\
                    self._wikidata.get_wiki_text("summarized_wiki_lead_section", wiki_id)

    def _process(self, pre_build_file_path, post_build_file_path):
        with open(pre_build_file_path, "r") as pre_build_file:
            reading_sets = json.load(pre_build_file)

        for conversation_id in tqdm(reading_sets.keys()):

            article_url = reading_sets[conversation_id]["article_url"]
            del reading_sets[conversation_id]["article_url"]

            if reading_sets[conversation_id]["config"] != "C":
                reading_sets[conversation_id]["article"] = self._get_article_section(article_url)
            else:
                reading_sets[conversation_id]["article"] = {"url": article_url}

            for agent in self._agents:
                # populate factual section for each agent corresponding to the conversation_id
                self._populate_factual_section(reading_sets, conversation_id, agent)

        with open(post_build_file_path, "w") as post_build_file:
            post_build_file.write(json.dumps(reading_sets, indent=2))

    def build(self):
        for file_name in os.listdir(self._pre_build_dir):
            pre_build_file_path = os.path.join(self._pre_build_dir, file_name)
            post_build_file_path = os.path.join(self._post_build_dir, file_name)

            if not os.path.isfile(post_build_file_path):  # if the file hasn't already been built from a previous run
                print("Begin processing file:", file_name)
                self._process(pre_build_file_path, post_build_file_path)
                print("Finished processing file:", file_name)

    def verify(self):

        with open(self._post_build_hashes, "r") as post_build_hashes_file:
            post_build_hashes = json.load(post_build_hashes_file)

            for file_name in os.listdir(self._post_build_dir):
                post_build_file_path = os.path.join(self._post_build_dir, file_name)
                with open(post_build_file_path, "rb") as post_build_file:
                    data = post_build_file.read()
                    md5_returned = hashlib.md5(data).hexdigest()
                    print("Verifying file:", file_name)
                    if md5_returned != post_build_hashes[file_name]:
                        print("Warning: Expected", post_build_hashes[file_name], "Returned", md5_returned)
                    else:
                        print("Successfully verified file:", file_name)


if __name__ == "__main__":
    builder = TopicalChatBuilder()
    builder.build()
    builder.verify()

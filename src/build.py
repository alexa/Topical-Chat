# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT
import json
import os
import argparse
from reddit.prawler import Prawler
from wapo.wapo_retriever import WapoRetriever
from wiki.wiki_data import WikiData
from tqdm import tqdm
import hashlib


def get_wiki_text(key, wiki_id, wikidata):
    return wikidata.get_wiki_text(key, wiki_id)


def get_text_from_thread_id(reddit_thread_id, prawler, reddit_id_to_text_mapping):

    if reddit_thread_id not in reddit_id_to_text_mapping.keys():
        reddit_id_to_text_mapping[reddit_thread_id] = prawler.get(reddit_thread_id)

    return reddit_id_to_text_mapping[reddit_thread_id]


def get_fun_facts_text_from_thread_id(reading_set, key, agent, fact_section_key, prawler, reddit_id_to_text_mapping):
    fun_facts_reddit_thread_id = reading_set[key][agent][fact_section_key]['fun_facts']
    fun_facts_text = []
    for thread_id in fun_facts_reddit_thread_id:
        fun_facts_text.append(get_text_from_thread_id(thread_id, prawler, reddit_id_to_text_mapping))
    return fun_facts_text


def get_fun_facts_text_and_wiki_text_for_all_fact_sections(reading_set, key, agent, prawler, reddit_id_to_text_mapping,
                                                           wikidata):
    fact_section_keys = ['FS1', 'FS2', 'FS3']
    for fact_section_key in fact_section_keys:
        reading_set[key][agent][fact_section_key]['fun_facts'] = get_fun_facts_text_from_thread_id(reading_set, key, agent, fact_section_key, prawler, reddit_id_to_text_mapping)

        # filling wiki section
        if 'shortened_wiki_lead_section' in reading_set[key][agent][fact_section_key]:
            wiki_id = reading_set[key][agent][fact_section_key]['shortened_wiki_lead_section']
            reading_set[key][agent][fact_section_key]['shortened_wiki_lead_section'] = get_wiki_text('shortened_wiki_lead_section', wiki_id, wikidata)

        if 'summarized_wiki_lead_section' in reading_set[key][agent][fact_section_key]:
            wiki_id = reading_set[key][agent][fact_section_key]['summarized_wiki_lead_section']
            reading_set[key][agent][fact_section_key]['summarized_wiki_lead_section']= get_wiki_text('summarized_wiki_lead_section', wiki_id, wikidata)

    return reading_set[key][agent]


def create_post_built_reading_set_file(input_directory, output_directory, filename, reddit_id_to_text_mapping,
                                       article_url_to_content_mapping, prawler, wapo_retriever, wikidata ):


    with open(os.path.join(input_directory, filename), 'r') as reading_set_input_file:
        reading_set = json.load(reading_set_input_file)

    with open(os.path.join(output_directory, filename), 'w') as reading_set_output_file:
        for key in tqdm(reading_set.keys()):
            article_url = reading_set[key]['article_url']
            del reading_set[key]['article_url']
            if article_url is not None and reading_set[key]['config'] is not "C":
                if article_url not in article_url_to_content_mapping.keys():
                    topical_content_wapo_section = wapo_retriever.get_wapo_article_section(article_url)
                    article_url_to_content_mapping[article_url] = topical_content_wapo_section
                else:
                    topical_content_wapo_section = article_url_to_content_mapping[article_url]

                reading_set[key]['article'] = {'url': article_url,
                                               'headline': topical_content_wapo_section['headline'],
                                               'AS1': topical_content_wapo_section['AS1'],
                                               'AS2': topical_content_wapo_section['AS2'],
                                               'AS3': topical_content_wapo_section['AS3'],
                                               'AS4': topical_content_wapo_section['AS4']
                                               }
            elif article_url is not None and reading_set[key]['config'] is "C" :
                reading_set[key]['article'] = {'url': article_url}
            else:
                reading_set[key]['article'] = {}

            # Getting text from fun facts thread id using reddit api
            agent_keys = ['agent_1', 'agent_2']
            for agent in agent_keys:
                reading_set[key][agent] = get_fun_facts_text_and_wiki_text_for_all_fact_sections(reading_set, key, agent,
                                                                                                 prawler,
                                                                                                 reddit_id_to_text_mapping,
                                                                                                 wikidata)

        reading_set_output_file.write(json.dumps(reading_set, indent=2))


def verify(reading_set_post_build_folder):
    hash_file_path = os.path.join(reading_set_post_build_folder , 'post_build_file_hashes.json')
    generated_post_build_reading_set_files = ['test_freq.json', 'test_rare.json', 'train.json', 'valid_freq.json', 'valid_rare.json']
    with open(hash_file_path, "r") as post_build_hashes_file:
        post_build_hashes = json.load(post_build_hashes_file)

        for file_name in generated_post_build_reading_set_files:
            post_build_file_path = os.path.join(reading_set_post_build_folder, file_name)
            with open(post_build_file_path, "rb") as post_build_file:
                data = post_build_file.read()
                md5_returned = hashlib.md5(data).hexdigest()
                print("Verifying file:", file_name)
                if md5_returned != post_build_hashes[file_name]:
                    print("Warning: Expected", post_build_hashes[file_name], "Returned", md5_returned)
                else:
                    print("Successfully verified file:", file_name)


def main():
    parser = argparse.ArgumentParser(description='Creation of Post built files')
    parser.add_argument('--reddit_client_id', help='You can obtain your client ID '
                                                   'and client secret by signing '
                                                   'up for Reddit credentials here: https://www.reddit.com', dest='CLIENT_ID', required=True)
    parser.add_argument('--reddit_client_secret', help='You can obtain your client ID '
                                                       'and client secret by signing '
                                                       'up for Reddit credentials here: https://www.reddit.com', dest='CLIENT_SECRET', required=True)
    parser.add_argument('--reddit_user_agent', help='Please supply any user agent', dest='USER_AGENT', required=True)
    opt = parser.parse_args()

    reading_set_pre_build_directory = '../reading_sets/pre-build/'
    reading_set_post_build_directory = '../reading_sets/post-build/'
    reddit_id_to_text_mapping = {}
    article_url_to_content_mapping = {}
    prawler = Prawler(opt.CLIENT_ID, opt.CLIENT_SECRET, opt.USER_AGENT)
    wapo_retriever = WapoRetriever()
    wikidata = WikiData()
    for filename in os.listdir(reading_set_pre_build_directory):
        print("Begin processing file:", filename)
        create_post_built_reading_set_file(reading_set_pre_build_directory, reading_set_post_build_directory, filename,
                                           reddit_id_to_text_mapping, article_url_to_content_mapping, prawler,
                                           wapo_retriever, wikidata)
        print("Finished processing file:", filename)

    verify(reading_set_post_build_directory)
if __name__ == "__main__":
    main()

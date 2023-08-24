# Enriched Topical-Chat: A Dialogue Act and Knowledge Sentence annotated version of Topical-Chat

This README describes Enriched Topical-Chat, an augmentation of Topical-Chat that contains dialogue act and knowledge sentence annotations for each turn in the dataset. Each annotation is automatically annotated using off-the-shelf models.

## Knowledge Sentence Annoations

Each conversation in Topical-Chat has a pair of reading sets which consists of a set of knowledge sentences. For every turn and knowledge sentence in the Topical-Chat dataset, we computed a TFIDF vector. We then computed the cosine similarity between a turn in the conversation and selected the top-1 knowledge sentence. In the new data release, for each conversation turn, we will present the knowledge sentences selected along with the similarity score.

## Dialogue Act Annoations

We obtain the dialogue acts for each turn by running an off-the-shelf SVM dialogue act tagger released by (https://github.com/ColingPaper2018/DialogueAct-Tagger). 
This tagger was trained on five datasets (Switchboard, Oasis BT, Maptask, VerbMobil2, AMI).

## Prerequisites

After cloning the repo you must first follow the instructions in https://github.com/alexa/Topical-Chat/blob/master/README.md. This includes building the original dataset along with the reading sets. Look at the Build Section for the exact steps. Once the original dataset is built each .json file will contain pointers to the knowledge sentences in the reading sets.

### Conversations:
The data is hosted on s3. To pull the data run these commands: 
```
wget https://enriched-topical-chat.s3.amazonaws.com/train.json

wget https://enriched-topical-chat.s3.amazonaws.com/valid_freq.json

wget https://enriched-topical-chat.s3.amazonaws.com/valid_rare.json

wget https://enriched-topical-chat.s3.amazonaws.com/test_freq.json

wget https://enriched-topical-chat.s3.amazonaws.com/test_rare.json
```

Each .json file has the specified format:
    
```    
{
  "t_d004c097-424d-45d4-8f91-833d85c2da31": {
    "article_url": "<link to washington post article>",
    "config": "C",
    "content": [
      {
        "message": ["Did you know that the University of Iowa's locker room is 
                    painted pink?", "I wonder why?"],
        "agent": "agent_1",
        "segmented_annotations": [
            {
                "da": "PropQ",
                "gt_ks": {"score": 0.73,"ds": "wiki", 
                "section": "FS1", "start_index": 0, "end_index": 100},
            }, 
            {
                "da": "ChoiceQ",
                "gt_ks": {"score": 0.0, "ds": "article", "section": "AS4", 
                          "start_index": 0, "end_index": 100},
            }
        ],
        "gt_turn_ks": {"score": 0.67, "ds": "fun_facts", 
                       "section": "FS1", "index": 0}
      },
``` 
```
The additional fields are:

message: a list containing the segments of each turn
segmented_annotations: a list of annotations for each segment within a turn each.
    da: ground truth dialog act associated with segmented response
    gt_ks: ground truth knowledge sentence associated with segmented response
        ds: data source knowledge retrieved from. wiki, fun_facts or article           
           fun_facts:
               section: which section containing the fun facts i.e. FS1
               index: which element in the list of fun facts
           wiki:
                section: which section containing the wikipedia sentence i.e. FS2
                start_index: index of beginning character of sentence in article
                end_index: index of end character
           article:
                section: which section of article. i.e. AS4
                start_index: index of beginning character of sentence in article
                end_index: index of end character
gt_turn_ks: ground truth knowlege sentence associated with turn
```

## Citation
If you use this dataset, please cite the following two papers:
### Enriched Topical-Chat
```
@article{hedayatnia2020policy,
  title={Policy-Driven Neural Response Generation for Knowledge-Grounded Dialogue Systems},
  author={Hedayatnia, Behnam and Gopalakrishnan, Karthik and Kim, Seokhwan and Liu, Yang and Eric, Mihail and Hakkani-Tur, Dilek},
  journal={arXiv preprint arXiv:2005.12529},
  year={2020}
}

```
### Topical-Chat
```
@inproceedings{gopalakrishnan2019topical,
  author={Gopalakrishnan, Karthik and Hedayatnia, Behnam and Chen, Qinlang and Gottardi, Anna and Kwatra, Sanjeev and Venkatesh, Anu and Gabriel, Raefer and Hakkani-Tür, Dilek},
  title={{Topical-Chat: Towards Knowledge-Grounded Open-Domain Conversations}},
  year={2019},
  booktitle={INTERSPEECH}
}

```

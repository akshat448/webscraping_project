import pandas as pd
import numpy as np
import os
import spacy
from spacy import displacy
import networkx as nx

import matplotlib.pyplot as plt

df = pd.read_csv('characters.csv')


# function to create a spacy model and read a book
def ner(file_name):
    # Load spacy English languague model
    nlp = spacy.load("en_core_web_sm")
    book_text = open(file_name, encoding='utf-8').read()
    book_doc = nlp(book_text)
    
    return book_doc


# function to get a dataframe of the characters in a book
def get_char_in_sentence(spacy_doc):
    sent_list = []  
    for sent in spacy_doc.sents:  
        character_list = [ent.text for ent in sent.ents]
        sent_list.append({"sentence": sent, "Characters": character_list})
        
    sent_df = pd.DataFrame(sent_list) 
    return sent_df


# function to filter out sentences with no characters
def filter_df(sent_df, df):
    
    return [char for char in sent_df 
            if char in list(df.character) 
            or char in list(df.character_firstname)]


# function create relationships between characters
def relations(df, window_size):
    relationships = []
    for i in range(df.index[-1]):
        print("DataFrame size:", len(df))
        print("DataFrame indices:", df.index)
        print("Last index:", df.index[-1])

        end_i = min(i+window_size, df.index[-1])
        char_list = sum((df.loc[i: end_i].character_name), [])

        # remove duplicated character names 
        char_unique = [char_list[i] for i in range(len(char_list))
                    if (i==0) or char_list[i] != char_list[i-1] ]

        if len(char_unique) > 1:
            for idx, a in enumerate(char_unique[:-1]):
                b = char_unique[idx+1]
                relationships.append({"source": a, "target": b})

    relationship_df = pd.DataFrame(relationships)
    # Sort the cases with a->b and b->a
    relationship_df = pd.DataFrame(np.sort(relationship_df.values, axis = 1), 
                                   columns = relationship_df.columns)
    relationship_df["value"] = 1
    relationship_df = relationship_df.groupby(["source","target"], 
                                              sort=False, 
                                              as_index=False).sum()
                
    return relationship_df
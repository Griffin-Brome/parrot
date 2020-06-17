import re
import json
import random
import argparse

def read_file(filename): 
    """Create list of all words in doc from a file."""
    words = []
    try:
        with open(filename,'r') as infile:
            for line in infile:
                for word in re.split(r'[^a-zA-Z0-9]+',line):
                    # only words should be added
                    if word.strip() and len(word) <= 50:                    
                        words.append(word.lower())
    except Exception as e:
        print(e)
    return words

def text_to_dict(word_list): 
    """
    Save words to dictionary.

    Each key/value pair in the dictionary is composed of a word and any words
    that immediately succeed it.
    """
    words = {}
    for i, word in enumerate(word_list):
        if word not in words:
            words[word] = []
        try:
            if word_list[i+1] not in words[word]: 
                words[word].append(word_list[i+1])
        except:
            continue
    with open('./var/www/json.txt','w+') as outfile:
        json.dump(words, outfile)

def gen_sentence(num_words=10):  
    """
    Populate a sentence using data from the JSON file

    For num_words iterations, fetch a random key from the dictionary, append it
    to the sentence, then fetch a random key from its associated list and
    append it as well. Then fetch a random key its associated list, and so on
    and so forth
    """
    sentence = ''
    try:
        with open('./var/www/json.txt','r') as infile:
            words = json.load(infile)
    except FileNotFoundError:
        return('Error: File not found, have you uploaded a .txt file?')
    
    rand_key = random.choice(words.keys())
    
    for i in range(num_words):
        if i == 0: # first word should be capitalized
            sentence = rand_key.capitalize()
        else:
            sentence = sentence + ' ' + rand_key
        if len(words[rand_key]) == 0:
            rand_key = random.choice(list(words.keys()))
        else:
            rand = random.randint(0,len(words[rand_key])-1)
            rand_key = words[rand_key][rand]
    return sentence + '.'

def gen_paragraph(length=10): 
    """Generate n paragraphs, using gen_sentence."""
    paragraphs = ""
    for j in range(length):
        if j == 0:
            paragraphs = '  ' + gen_sentence() + ' '
        else:    
            paragraphs = paragraphs + gen_sentence() + ' '
    return paragraphs

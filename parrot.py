#_____      ____________ _____ _____ 
#| ___ \____ | ___ \ ___ \  _  |_   _|
#| |_/ / __ \| |_/ / |_/ / |/' | | |  
#|  __/ / _` |    /|    /|  /| | | |  
#| | | | (_| | |\ \| |\ \\ |_/ / | |  
#\_|  \ \__,_\_| \_\_| \_|\___/  \_/  
#      \____/                    
# Griffin Brome 2019
import re
import json
import random

def process_input():
    file_name = input("Enter a file name: ")
    words = read_file(file_name)
    word_pairs = text_to_dict(words)        
    save_to_json(word_pairs)

def read_file(file_name): # Create list of all words in doc 
    words = []
    try:
        with open(file_name, "r") as infile:
            for line in infile:
                for word in re.split(r"[^a-zA-Z0-9]+",line):
                    if word.strip(): # only words should be added                   
                        words.append(word.lower())
    except Exception as e:
        #print("error: file not read/does not exist")
        print(e)
    return words

def text_to_dict(word_list): # Save words to dictionary in order to send to JSON
    words = {}
    for i, word in enumerate(word_list):
        if word not in words:
            words[word] = []
        try:
            if word_list[i+1] not in words[word]: 
                words[word].append(word_list[i+1])
        except:
            continue
    return words

def save_to_json(dict): #TODO make this specific to last uploaded file
    with open('json.txt', 'w+') as outfile:
        json.dump(dict, outfile)

def gen_sentence(num_words=10):  
    sentence = ''
    try:
        with open('json.txt', 'r') as infile:
            words = json.load(infile)
    except FileNotFoundError:
        print("Error: File not found, have you uploaded a .txt file?")
    
    rand_key = get_rand_key(list(words.keys()))
    
    for i in range(num_words):
        if i == 0: # first word should be capitalized
            sentence = rand_key.capitalize()
        else:
            sentence = sentence + " " + rand_key
        if len(words[rand_key]) == 0:
            rand_key = get_rand_key(list(words.keys()))
        else:
            rand = random.randint(0,len(words[rand_key])-1)
            rand_key = words[rand_key][rand]
    return sentence + '.'

def get_rand_key(key_list): 
    rand = random.randint(0, len(key_list))
    return key_list[rand]

def gen_paragraph(length=10): 
    paragraphs = ""
    for j in range(length):
        if j == 0:
            paragraphs = "  "+ gen_sentence() + " "
        else:    
            paragraphs = paragraphs + gen_sentence() + " "
    return paragraphs
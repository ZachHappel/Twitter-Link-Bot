from __future__ import unicode_literals
import pytesseract
import time
from PIL import Image, ImageEnhance, ImageFilter, ImageFile
import urllib2
import praw
from imgurpython import ImgurClient
from bs4 import BeautifulSoup
import requests
from imgur_connect import imgurConnect
from functions import *
from image_reader import getText, findParams

import enchant
import itertools



#Remove Spell Check! Already done in image reader!



def get_screenname_variations(username, character):

    combinations_to_return = []


    def get_username_list():

        username_list = []

        for adding in range(0, len(username)):

            if '.' == username[adding]:
                pass
            elif '@' == username[adding]:
                pass
            else:
                username_list.append(username[adding])

        return username_list



    def create_vars_add(char, count, username_list):    #Adding extra "-"/"_"
        locations = []

        to_add = char*count

        modified_username_list = username_list
        print("Username List: "+str(username_list))
        for search in range(0, len(username)):
            if username[search] == char:
                locations.append(search)

        for location in range(0, len(locations)):
            modified_username_list.insert(locations[location], to_add)


        return modified_username_list



    def create_vars_sub(char, count, username_list):    #Subtracting extra "-"/"_"
        locations = []


        modified_username_list = username_list
        print("Username List: "+str(username_list))
        for search in range(0, len(username)):
            if username[search] == char:
                locations.append(search)

        for location in range(0, len(locations)):
            print(locations[location])
            modified_username_list.pop(locations[location])


        return modified_username_list

  #     Handling '-' '_' characters     #

    #            Adding               #
    username_list = get_username_list()
    if character != ' ':
        new_username_list = (create_vars_add(character, 1, username_list))
        combination = ''.join(new_username_list)
        combinations_to_return.append(combination)
        new_username_list = (create_vars_add(character, 2, username_list))
        combination = ''.join(new_username_list)
        combinations_to_return.append(combination)
        new_username_list = (create_vars_sub(character, 2, username_list))
        combination = ''.join(new_username_list)
        combinations_to_return.append(combination)

    #          Subtracting           #

    #           Other               #
    if username[len(username)-1] == 'a':                          #Creating combinations without the 'a' at the end
        combinations_to_return.append(username)                   #Some mobile screenshots will appear to have an 'a' at the end if verified symbol is present
        for searching in range(0, len(combinations_to_return)):
            selected_username = combinations_to_return[searching]
            combinations_to_return.append(selected_username[:len(selected_username)-1])
    else:
        pass

    return combinations_to_return


#print(get_screenname_variations("zach--happela"))


def get_tweet_variations(tweet_text):
    english_dictionary = enchant.Dict("en_US")
    splitted_tweet = tweet_text.split()

    spell_checked = []
    combinations = []

    for searching in range(0, len(splitted_tweet)):    #Spell check to remove any words that may have been read incorrectly
        word = splitted_tweet[searching]
        isWord = english_dictionary.check(word)
        if isWord:
            spell_checked.append(word)
        else:
            pass


    def reset_list():   #Python was being difficult
        new_list = []
        for x in range(0, len(spell_checked)):
            new_list.append(spell_checked[x])
        return new_list


    for search in range(0, len(spell_checked)):
        new_list = reset_list()   #Gross, I know.
        new_list.pop(search)
        if search == len(spell_checked):
            sentence = ''
            for x in range(0, len(spell_checked)-1):
                sentence = sentence + str(spell_checked[x])
            combinations.append(sentence)
        else:
            pass

        combinations.append(' '.join(new_list))


    return (combinations)

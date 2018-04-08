import pytesseract
import time
import urllib2
import praw
from imgurpython import ImgurClient
from bs4 import BeautifulSoup
import requests
from PIL import Image, ImageEnhance, ImageFilter, ImageFile
import numpy as np
import cv2
import argparse
import StringIO
import PIL
import enchant
english_dict = enchant.Dict("en_US")


symbols = [",",".","'","/","=","."," "]

def findParams(splittedText):
                                            # twitterHandle
                                            # firstLine
    number = 0
    twitterHandle = ''
    firstLine = ''

    def get_username(splittedText): #Finds username by searching for first '@' symbol in text

        not_found = True

        for searching in range(0, len(splittedText)):

            line = splittedText[searching].split()

            for word in range(0, len(line)):
                selected_word = line[word]
                #print("This is selected word: " +selected_word)
                if '@' in selected_word:

                    for letter in range(0, len(selected_word)):

                        if '@' == selected_word[letter]:
                            starting_char = letter
                            twitter_handle = selected_word[starting_char:]
                            print("Found Twitter Handle: "+twitter_handle)
                            line_found_on = searching
                            not_found = False
                            return (twitter_handle, line_found_on)

                        else:
                            pass
                else:
                    pass


        #if not_found == False:
            #return (twitter_handle, line_found_on)

        if not_found == True:
            return ("Twitter Handle Not Found", 'Cancel Operation')



    def find_viable_lines(splittedText, twitter_handle_line): #Find lines that aren't largely made up of numbers

        viable_lines = []
        numbers = 0

        for lineSearch in range((twitter_handle_line)+1, len(splittedText)):
            line_being_searched = splittedText[lineSearch]

            for char_search in range(0, len(line_being_searched)):
                char = line_being_searched[char_search]   #Character in Word

                if char.isalpha():
                    pass
                else:
                    numbers +=1

            if numbers >= (len(line_being_searched)/2):
                pass
            else:
                viable_lines.append(line_being_searched)
                numbers = 0


        return viable_lines




    def spell_check_lines(viable_lines): #Parses lines and removes words that were most likely interpreted incorrectly

        spell_checked_lines_list = []

        for lines in range(0, len(viable_lines)):
            line = viable_lines[lines]
            new_line = ''
            words = line.split()
            print("Spell checking line #"+str(lines))
            all_words_good = True
            for word in range(0, len(words)):
                if english_dict.check(words[word]):
                    new_line = new_line + " "+ words[word]
                else:
                    pass

            spell_checked_lines_list.append(new_line)

        return spell_checked_lines_list



    def get_search_terms(spell_checked):  #Only use lines larger than or equal to three lines

        #Checking how many words are in the spell checked lines

        if len(spell_checked) >= 3:
            search_terms = spell_checked[0] + spell_checked[1]   # Combine two lines in order to (hopefully) increase odds of finding the tweet
        else:
            try:
                search_terms = spell_checked[0]
            except:
                return ' '

        return search_terms
    print("Getting Username...")
    find_twitter_handle = get_username(splittedText)
    twitter_handle = find_twitter_handle[0]
    twitter_handle_line = find_twitter_handle[1] #The line where the username was found, it is noted because we need to now look at the body of the tweet
    #print("Twitter Handle Line Number" + twitter_handle_line)
    if twitter_handle == "Twitter Handle Not Found":
        print('Twitter Handle Not Found')
        return ("Cancel Operation", "Twitter Handle Not Found")

    else:
        print("Getting lines of tweet...")
        body = find_viable_lines(splittedText, twitter_handle_line)
        body = spell_check_lines(body)
        words_for_query = get_search_terms(body)

        return (twitter_handle, words_for_query)





def getText(img):
    pic = cv2.imread(img)
    lower = np.array([219, 219, 219])  #Lower limit of RGB Values ==> Gray Color
    upper = np.array([255, 255, 255])  #Upper limit of RGB Values ==> White Color
    shapeMask = cv2.inRange(pic, lower, upper)
    _, contours, _ = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imwrite("masked.png", shapeMask)  # Save Edited Picture as Masked.PNG
    text = pytesseract.image_to_string(Image.open("masked.png"))  # raw text from image



    if '@' in text:

        splitted = text.split('\n')  # Split into list, each variable in the list is a new line in the searched text

        tweetTuple = findParams(splitted) #Parses text for screenname and for first line

        if tweetTuple[0] == 'Cancel Operation':
            return ('Cancel Operation', '')
        else:
            print("Passing tweet tuple to Variations")
            print("Tweet Tup : " +str(tweetTuple))

            outcome_of_image_reader = ('True', tweetTuple)  # <----,

            return outcome_of_image_reader                  # <---- Returned to operations.py


    else:

        outcome_of_image_reader = ('Cancel Operation', '') # <----,

        return(outcome_of_image_reader)         # <---- Returned to operations.py







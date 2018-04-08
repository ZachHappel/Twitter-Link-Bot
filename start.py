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
from size import get_image_size
from functions import *
from image_reader import getText, findParams                 #Change Back !!!!!!!!!!!!!!
from variations import get_screenname_variations, get_tweet_variations  #Change Back !!!!!!!!!!!!!!
from newestTwitterSearch import find_tweet


used_links = []
new_links = []
reset_everytime = []


class reddit_Posts:
    post_archive = []



client = ImgurClient(connectToImgur.client_id, connectToImgur.client_secret)


def clear_new_links():
    global new_links
    new_links = []

def check_r_all(bot):
    global post_archive
    response_from_reddit = load_all_new(bot)    #Gets links from Subreddit
    links = response_from_reddit[0]
    reddit_Posts.post_archive = response_from_reddit[1]
    #for reddit_posts in range(links):

    return links


def sequence_of_events(new_links):
    for checking in range(0,len(new_links)):    #Checks Links



        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        link_to_be_checked = new_links[checking]   #Checks link in the new link list

        if 'gif' in link_to_be_checked:
            break
        else:
            pass


        print("Unprocessed Link: "+ link_to_be_checked)  #Print link being tested
        response_from_check = get_direct_link(link_to_be_checked) #Gets the direct Imgur Link
        print("Direct Link: "+str(response_from_check))   #LETS US KNOW IF IT IS AN IMGUR LINK


        if 'gif' in response_from_check:
            break
        else:
            pass


        if response_from_check == 'NO':  #If NO(t) an image from imgur or redd.it --> Skip the link
            pass


        else:

            print("This is image size: " + str(get_image_size(response_from_check)))

            saveImage(response_from_check, 'to_be_checked.jpg')   #Saves image

            fulltweet_text = getText("to_be_checked.jpg")                    #Grabs text from it



            if fulltweet_text[0] == 'Cancel Operation':                                 #False = Not a Tweet
                print("Not a Tweet.")


            else:
                print(fulltweet_text)   #Print the Tuple ('True/False', *Tweet*)
                tweet_tuple = fulltweet_text[1]
                username = tweet_tuple[0]
                tweet_firstline = tweet_tuple[1]






                splitted_firstline = tweet_firstline.split()  #EW
                new = []
                if len(splitted_firstline) > 5:
                    for x in range(0, len(splitted_firstline)):
                        new.append(splitted_firstline[x])

                    tweet_firstline = ' '.join(new)
                else:
                    pass




                #if len(tweet_firstline.split(' ')) > 4:
                tweet_firstline_combos = get_tweet_variations(tweet_firstline)
                tweet_firstline_combos.append(tweet_firstline)
                #else: #Won't perform removal, combination operation if the line is too short
                #    tweet_firstline_combos = tweet_firstline

                if '-' in username:
                    username_combos = get_screenname_variations(username, '-')
                    print("Username Combos: \n" + str(username_combos))
                elif '_' in username:
                    username_combos = get_screenname_variations(username, '_')
                    print("Username Combos: \n" + str(username_combos))
                else:
                    username_combos = get_screenname_variations(username, '')
                    print("Username Combos: \n" + str(username_combos))

                print("Tweet Combos: \n" + str(tweet_firstline_combos))


                check_if_all_username_combos_are_same = True
                for usernames in range(0, len(username_combos)):
                    if username_combos[usernames] == username:
                        check_if_all_username_combos_are_same = True

                        if usernames == len(username_combos): #Last check tells us if they are all the same
                            print("All usernames are the same")
                    else:
                        check_if_all_username_combos_are_same = False
                        print("Different usernames; combinations were successfully made.")

                #if check_if_all_username_combos_are_same:
                username_list = []
                username_list.append(username_combos[0])

                tweet_link = (find_tweet(username_list, tweet_firstline_combos)) #Try to find link to tweet

                if tweet_link == "Tweepy Search Results: None":
                    return
                else:
                    if (tweet_link) == None:
                        pass
                    else:
                        post_used_to_comment = reddit_Posts.post_archive[checking]
                        post_used_to_comment.reply('Direct link to [**tweet**](%s)'%tweet_link)
                        print('Comment posted.')
                #else:
                  #  pass
                    #print(find_tweet(username_combos, tweet_firstline_combos))










while True:
    try:
        get_links_bot1 = check_r_all(connectBot.commentBot)  #Gets URls from r/all/new

        for link in range(0, len(get_links_bot1)):
            if get_links_bot1[link] in used_links:
                pass
            else:
                new_links.append(get_links_bot1[link]) #adds them to list to be checked
                used_links.append(get_links_bot1[link]) #adds to used link so it wont be reused
                reset_everytime.append(get_links_bot1[link]) #Change eventually


        sequence_of_events(new_links)
        clear_new_links()


        if len(used_links) >= 100:
            used_links = []

        reset_everytime = []
        time.sleep(1)
    except:
        print("Failed")
        clear_new_links()
        sequence_of_events(new_links)
        pass



from __future__ import unicode_literals

import time
import sys


from reddit_main import Reddit_Main
from imgur_main import Imgur_Main
from twitter_main import Twitter_Main
from ocr import performOCR
from text_parsing import parse_text
from text_variations import get_screenname_variations, get_tweet_variations
from local_logging import Logging


#Image downloading and URL checking is done within imgur_main
#Object imgurInstance is how we access all of them

client_id = ''
client_secret = ''
#Imgur

imgurInstance = Imgur_Main(client_id, client_secret)
redditBot = Reddit_Main('bot1')
logging = Logging()

consumer_key = ""
consumer_secret = ""
access_token_key = ""
access_token_secret = ""
Twitter = Twitter_Main(consumer_key, consumer_secret, access_token_key, access_token_secret)
#Twitter



def processURL(url_to_be_checked, image_number):

    if imgurInstance.checkURL(url_to_be_checked) is None:
        return None  # If None, parameters for the URL were not met
    else:
        try:
            direct_url = imgurInstance.get_direct_link(url_to_be_checked)
        except Exception as e:
            logging.logError(e)
            return None


    if direct_url is None:
        return None
    else:

        image_name = 'image_' + str(image_number) + '.jpg'
        imgurInstance.saveImage(direct_url, image_name)

        ocrResults = performOCR(image_name)
        parseResults = parse_text(ocrResults)

        if parseResults is None:
            return None

        twitter_handle = parseResults[0]
        tweet_body = parseResults[1]

        print("Tweet Body: " + str(tweet_body))

        if twitter_handle is None or tweet_body is None:
            return None


        print("Twitter Handle Found: "+twitter_handle)
        print("Tweet Body Found: "+str(tweet_body))

        if twitter_handle is None or tweet_body is None: return None

        else:    #Create variations of both tweet_body and twitter_handle

            tweet_variations = get_tweet_variations(tweet_body)

            if '-' in twitter_handle:
                username_variations = get_screenname_variations(twitter_handle, '-')
            elif '_' in twitter_handle:
                username_variations = get_screenname_variations(twitter_handle, '_')
            else:
                username_variations = [twitter_handle]


            print('Tweet Variations: '+str(tweet_variations))
            print("Username Variations: "+str(username_variations))

            combinations = Twitter.usernameTweetCombos(username_variations, tweet_variations)
            response = Twitter.tweepyCycleCombinations(combinations)
            return(response)


def cycleUrls():

    #redditBot.load_all_new()  # loads refreshed list of newest image submissions
    links = redditBot.getSubmissionsFromRAll()

    for checking in range(0, len(links)):

        content_link_and_reddit_link = links[checking]
        content_link = content_link_and_reddit_link[0]
        reddit_link = content_link_and_reddit_link[1]


        if content_link in redditBot.used_links:
            pass
        else:
            print("Content URL: " + content_link)
            print("Reddit URL: " + str(reddit_link))

            response = processURL(content_link, checking)
            redditBot.used_links[content_link] = reddit_link
            logging.logURLChecked(content_link)

            if response is None:
                pass
            else:
                link_to_tweet = response
                post_used_to_comment = reddit_link
                post_used_to_comment.reply('Direct link to [**tweet**](%s)' % link_to_tweet)
                print('Comment posted.')





def acquire_urls():

    try:
        refreshedURLs = redditBot.check_r_all()  # Gets URls from r/all/new
        for link in range(0, len(refreshedURLs)):
            url = refreshedURLs[link]
            if url in redditBot.postProcessedUrls or url in redditBot.preProcessedUrls: pass  #If link already tested
            else:

                redditBot.preProcessedUrls.append(url)  # Adds to preProcessed
                redditBot.postProcessedUrls.append(url)  # Adds to post-processed because it will be processed
                redditBot.reset_everytime.append(url)  # Change eventually

        cycleUrls()
        redditBot.clear_PreProcessed_Urls()
        if len(redditBot.postProcessedUrls) >= 100: redditBot.postProcessedUrls = []
        redditBot.reset_everytime = []
        time.sleep(1)

    except Exception as e:
        logging.logError(e)
        redditBot.clear_PreProcessed_Urls()
        acquire_urls()


if __name__ == '__main__':


    while True:
        acquire_urls()








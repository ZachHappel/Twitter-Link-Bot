from __future__ import unicode_literals
import time
from reddit_main import Reddit_Main
from imgur_main import Imgur_Main
from twitter_main import Twitter_Main
from ocr import performOCR
from text_parsing import parse_text
from text_variations import createTwitterHandleVariations, get_tweet_variations
from local_logging import Logging
from db_main import DB_Main
from ximilar_main import Ximilar_Main
print("Libraries successfully imported...")


client_id = ''
client_secret = ''
imgurInstance = Imgur_Main(client_id, client_secret)
redditBot = Reddit_Main('bot1')
database = DB_Main("", "", "")  #Connecting to MySQL Database
ximilar = Ximilar_Main()  #Ximilar API
consumer_key = ""
consumer_secret = ""
access_token_key = ""
access_token_secret = ""
Twitter = Twitter_Main(consumer_key, consumer_secret, access_token_key, access_token_secret)
logging = Logging()
print("Initialization successful...")


#Reddit Permalink: the link to the post on reddit itself. (e.g where comments can be made, users can upvote/downvote, etc.)

total_processed = 0

def processURL(url_to_be_checked, image_number):

    if imgurInstance.checkURL(url_to_be_checked) is None: return None  # If None, parameters for the URL were not met
    else:
        try:
            direct_url = imgurInstance.get_direct_link(url_to_be_checked)
        except Exception as e:
            logging.logError(e)
            return None


    if direct_url is None: return None
    else:
        image_name = 'image_' + str(image_number) + '.jpg'
        imgurInstance.saveImage(direct_url, image_name)
        ocrResults = performOCR(image_name)
        parseResults = parse_text(ocrResults) #Extracts text from image
        if parseResults is None: return None
        twitter_handle = parseResults[0]
        tweet_body = parseResults[1]  #Tweet body after it has been parsed
        if twitter_handle is None or tweet_body is None: return None
        else:
            tweet_variations = get_tweet_variations(tweet_body)                 #Variations of tweet body
            username_variations = createTwitterHandleVariations(twitter_handle) #Variations of twitter handle
            combinations = Twitter.usernameTweetCombos(username_variations, tweet_variations)
            response = Twitter.tweepyCycleCombinations(combinations)
            return(response)


def cycleUrls():
    print("Cycling new list")
    global total_processed



    db_links_list = []  #Links to be inserted into DB

    links = database.format(redditBot.getSubmissionsFromRAll()) #Get, and format, the latest hundred posts made to reddit.com
    total_processed = total_processed + len(links)              #Amount of links processed during current session

    for checking in range(0, len(links)):
        print(str(checking) + " of "+ str(len(links)) + " links") #Number of submissions found
        try:
            content_reddit_subreddit = links[checking] #Tuple (content_link, Submission, subreddit)
            content_link = content_reddit_subreddit[0] #URL to either: reddit self-post or outside website
            submission = content_reddit_subreddit[1]  #'submission' is the respective Submission object for the post in question
            subreddit = content_reddit_subreddit[2]   #Subreddit

            submission_permalink = submission.permalink

            #Check to see if link is within the local archive of links --> Prevents duplicate comments
            if submission_permalink in redditBot.used_links: pass
            else:
                redditBot.used_links[submission_permalink] = submission      #Adds to local archive of used links
                logging.logURLChecked(content_link)                          #Logs in txt file the link
                try:
                    response = processURL(content_link, checking) #Processing = Download, OCR, Varations, Tweet Search, etc.
                                                                  #Response is either the link to the tweet, or it is None
                except Exception as e:
                    print("Error while Processing: " + str(e))
                    response = None

                if response is None: #Do nothing other than add to the list that will be server archived
                    db_links_list.append([content_link, submission, subreddit, 0])  #0 refers to no tweet found
                else:
                    db_links_list.append([content_link, submission, subreddit, 1]) #1 refers to tweet found
                    link_to_tweet = response #Twitter.com link
                    ximilar_tweet_testing = ximilar.isImageTweet(content_link)

                    if ximilar_tweet_testing is True:
                        redditBot.postComment(submission, link_to_tweet)
                    else: continue

        except Exception as e:
            print("Error In Cycling: "+str(e))

    database.archiveURLsAndPosts(db_links_list)
    print("Amount Processed: " + str(total_processed))


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
        print("Error in Acquiring: " + str(e))
        logging.logError(e)
        redditBot.clear_PreProcessed_Urls()
        acquire_urls()

if __name__ == '__main__':
    while True:
        acquire_urls()








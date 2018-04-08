import pytesseract
import time
from PIL import Image, ImageEnhance, ImageFilter, ImageFile
import urllib2
import praw
from imgurpython import ImgurClient
from bs4 import BeautifulSoup
import requests
from imgur_connect import imgurConnect
from image_reader import getText, findParams
bot = praw.Reddit('bot1')  # Connecting to Reddit Account: twitterlinkbot
listOfCheckedLinks = []  # List to place used Imgur links


class connectBot:
    commentBot = praw.Reddit('bot1')
    #search_bot_2 = praw.Reddit('bot2')
    #search_bot_3 = praw.Reddit('bot3')

class connectToImgur:
    client_id = imgurConnect.client_id
    client_secret = imgurConnect.client_secret
    client = ImgurClient(client_id, client_secret)


client = ImgurClient(connectToImgur.client_id, connectToImgur.client_secret)

def load_all_new(bot):
    urls = []
    post_archive = []
    all = bot.subreddit('all')
    for post in all.new(limit=15):
        test = post
        post_url = post.url
        urls.append(post_url)
        post_archive.append(post)    #Archives the Post's so we can reply to them later
        #print(post.permalink)

    return (urls, post_archive)

def saveImage(directUrl, saveAs):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    response = requests.get(directUrl)
    if response.status_code == 200:
        print('Downloading...')
        with open(saveAs, 'wb') as data:
            for chunk in response.iter_content(4096):
                data.write(chunk)
            #print("Saved")

def get_direct_link(URL):
    #print("get_direct_link: "+ URL)


    def albumURL(URL):       #function to get direct image URL from Imgur Album URL
        findEnd = URL.rindex('/') + 1       # finds last '/' in the full, untouched/unchanged URL
        albumIdentifier= URL[findEnd:]      # gets end part of URL ex: https://imgur.com/a/mTpUT --> mTpUT
        album = connectToImgur.client.get_album_images(albumIdentifier)
        if len(album) > 1:   #If there is more than one picture in the album, it gets reject because it is most likely not a screenshot of a tweet
            return 'NO'
        else:
            for image in album:
                directURL = image.link        #directURL is the i.imgur.com link: a direct link to the picture
                return directURL                                #quits after because we are only going to accept one


    def normalURL(URL):
        findEnd = URL.rindex('/') + 1
        imageIdentifier = URL[findEnd:]
        picture = connectToImgur.client.get_image(imageIdentifier) # Picture is essentially a class for the picture, ex: .link, .id, etc.
        directURL = picture.link    #Direct url,  i.imgur.com
        #print("This is the direct link: " + directURL)
        return directURL
        #saveImage(directURL, 'downloaded.jpg')



    if "imgur.com/a/" in URL:    #Imgur URL and an Album
        #print("Album")
        return albumURL(URL)
    elif "i.imgur.com" in URL:  #already a direct link
        #print("Direct Link")
        #saveImage(URL, 'downloaded.jpg')
        return URL
    elif "i.redd.it" in URL:  #already a direct link
        #print("Direct Link")
        #saveImage(URL, 'downloaded.jpg')
        return URL
    elif "imgur.com" in URL:     #Imgur URL but not an Album
        #print("Standard Link")
        return normalURL(URL)
    else:
        print("Not an Imgur Link")
        return 'NO'                  # Not an Imgur URL


















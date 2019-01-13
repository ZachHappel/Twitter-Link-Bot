import requests
from PIL import Image, ImageEnhance, ImageFilter, ImageFile

from clients import ImgurConnection
from local_logging import Logging

class Imgur_Main:

    logging = Logging()

    def __init__(self, client_id, client_secret):
        try:
            self.imgurBot = ImgurConnection(client_id, client_secret).ImgurClientConnection
        except Exception as e:
            self.logging.error_log(e)



    def saveImage(self, directUrl, saveAs):  #working
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        response = requests.get(directUrl)
        if response.status_code == 200:
            print('Downloading...')
            with open(saveAs, 'wb') as data:
                for chunk in response.iter_content(4096):
                    data.write(chunk)
                    # print("Saved")


    def checkURL(self, URL):  #Returns None if URL is not an imgur post or a reddit self-posted image
                              #Also checks if .gif is within the URL -- in an effort to avoid them
        print("Checking: "+URL)
        if ('imgur' in URL) or ('i.redd.it' in URL):

            if '.gif' in URL or '.mp4' in URL or '.mov' in URL or '.tiff' in URL or '.apng' in URL or '.gifv' in URL or '.webm' in URL:
                print('None')
                return None
            else:
                print('Passed')
                return URL
        else:
            print('None')
            return None


    def get_direct_link(self, URL):
        # print("get_direct_link: "+ URL)

        def albumURL(URL):  # function to get direct image URL from Imgur Album URL
            findEnd = URL.rindex('/') + 1  # finds last '/' in the full, untouched/unchanged URL
            albumIdentifier = URL[findEnd:]  # gets end part of URL ex: https://imgur.com/a/mTpUT --> mTpUT
            album = self.imgurBot.get_album_images(albumIdentifier)
            if len(
                    album) > 1:  # If there is more than one picture in the album, it gets reject because it is most likely not a screenshot of a tweet
                return None
            else:
                for image in album:
                    directURL = image.link  # directURL is the i.imgur.com link: a direct link to the picture
                    return directURL  # quits after because we are only going to accept one

        def normalURL(URL):
            findEnd = URL.rindex('/') + 1
            imageIdentifier = URL[findEnd:]
            picture = self.imgurBot.get_image(imageIdentifier)  # Picture is essentially a class for the picture, ex: .link, .id, etc.
            directURL = picture.link  # Direct url,  i.imgur.com
            # print("This is the direct link: " + directURL)
            return directURL
            # saveImage(directURL, 'downloaded.jpg')

        if "imgur.com/a/" in URL:  # Imgur URL and an Album
            # print("Album")
            return albumURL(URL)
        elif "imgur.com/gallery/" in URL:
            URL = URL.replace("gallery", "a")
            return URL
        elif "i.imgur.com" in URL:  # already a direct link
            # print("Direct Link")
            # saveImage(URL, 'downloaded.jpg')
            return URL
        elif "i.redd.it" in URL:  # already a direct link
            # print("Direct Link")
            # saveImage(URL, 'downloaded.jpg')
            return URL
        elif "imgur.com" in URL:  # Imgur URL but not an Album
            # print("Standard Link")
            return normalURL(URL)
        else:
            print("Not an Imgur/Reddit self-posted image")
            return None # Not an Imgur URL




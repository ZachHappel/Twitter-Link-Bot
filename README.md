# Twitter-Link-Bot
### What is Reddit?  
Reddit is a community-driven social media platform divided up into subcommunities called subreddits.   
### What is a bot?
An automated user account that continuously performs operations, typically commenting it's results, in response to other
user's generated content in an effort to provide a meaningful and purposeful addition to the community at large.

### What does Twitter-Link-Bot do?  
Under the username **[twitterlinkbot](https://www.reddit.com/user/twitterlinkbot)**, the automated process returns a direct-url
to a tweet that was submitted to Reddit in the form of a screenshot - commenting among other users within the discussion section.

### How it works:
* Using the Reddit API, PRAW, a list of the latest one hundred submission are retrieved
* The submissions are sifted through and their viability is determined by the content of each respective post. If the
submission contains a link to a image-hosting website such as Imgur, or rather an image is simply uploaded directly to Reddit,
the submission continues on to the next step in the process.
* Using *requests*, chunks of data are stored and then saved as a JPEG image file
* Prior to Optical Character Recognition, a mask is applied to the image using *cv2*, making the OCR more precise
* *Pytesseract* is used to extract the text from the masked image
* Passing through several parsing functions that remove characters/words that are believed to be erroneous, if present,
a Twitter handle and along with the words found within the tweet (tweet body) are returned.
* Variations of the tweet body as well as the twitter handle are created
* Combinations of the variations are created and passed to the *tweepy* pre-search handler which checks to see if the user's
tweets have already been archived locally (these archives are reset every thirty minutes). If they have not, the latest 3200
tweets are stored and then archived.
* These tweets are then tested against the aforementioned comments and if particular parameters are met (relating to words found
in the image, and the tweet retrieved from twitter) a direct-url to the tweet is returned
* Finally, the last step before commenting the found link, the image is then tested against a model trained, using *Ximilar*, to identify Twitter screenshots.
In an effort to avoid reaching the API rate limit on their free tier, this step is done last.
* If a direct-link to the tweet is uncovered and the model determines the image as a tweet, the URL is posted in the comment section of the
submission corresponding to the image.




A more in-depth explanation of this entire process will be in an article that is soon to come. 

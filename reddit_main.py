from clients import RedditConnection
from local_logging import Logging

class Reddit_Main:

    logging = Logging()
    postProcessedUrls = []
    preProcessedUrls = []
    reset_everytime = []

    post_archive = []

    used_links = {}

    def __init__(self, name):
        self.redditBot = RedditConnection(name).RedditBot #bot1 is alias of reddit user in praw.ini
                                                #RedditBot is the actual connection

    def clear_PreProcessed_Urls(self):
        self.preProcessedUrls = []
        print('PreProcessed cleared')

    def check_r_all(self):
        response_from_reddit = self.load_all_new()  # Gets links from Subreddit
        links = response_from_reddit[0]
        self.post_archive = response_from_reddit[1]   #archives the posts returned
        # for reddit_posts in range(links):

        return links, self.post_archive
        # response_from_reddit = ([],[])
        # Where first list array is the link to the submission
        # And the second is the submission id of the post(?) -- may be of user


    def load_all_new(self): #working
        urls = []
        post_archive = []
        all = self.redditBot.subreddit('twitterbottestarea')
        for post in all.new(limit=15):
            post_url = post.url
            urls.append(post_url)
            post_archive.append(post)  # Archives the Post's so we can reply to them later


        return (urls, post_archive)


    def postComment(self, tweet_link, archive_index):
        post_used_to_comment = self.post_archive[archive_index]
        post_used_to_comment.reply('Direct link to [**tweet**](%s)' % tweet_link)
        self.logging.logComment(str(self.post_archive[archive_index]), tweet_link)
        print('Comment posted.')





    def getSubmissionsFromRAll(self):
        post_tuple_list = []
        posts = self.redditBot.subreddit('all')
        for post in posts.new(limit=15):
            tuple = (post.url, post) #url to either a reddit self text-post or external website, and the submission object itself
            post_tuple_list.append(tuple)

        return post_tuple_list


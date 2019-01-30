from clients import RedditConnection
from local_logging import Logging



class Reddit_Main:

    logging = Logging()
    postProcessedUrls = []
    preProcessedUrls = []
    reset_everytime = []

    post_archive = []

    used_links = {}



    nsfw_subreddits = {}

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


    def postComment(self, submission, link):
            comment = "Direct link to [**tweet**](%s) \n" \
                      "***\n" \
                      "^(This is a bot.     Am I a 'Good bot'?     All feedback is appreciated!)" % link
            submission.reply(comment)  # Comment on post using 'submission', the Submission object
            print('Comment posted.')


    def getSubmissionsFromRAll(self):
        post_tuple_list = []
        posts = self.redditBot.subreddit('all')
        for post in posts.new(limit=100):
            tuple = (post.url, post) #url to either a reddit self text-post or external website, and the submission object itself
            post_tuple_list.append(tuple)

        return post_tuple_list


    def removeNSFWSubreddits(self, submissions_found): #Getting over18 classifier from Reddit is timely
                                                       #so we create an index of them. Only once is the request to reddit
                                                       #required.
        non_nsfw_posts = []
        for post in submissions_found:
            subreddit = post[1].subreddit
            str_subreddit = str(subreddit)
            if str_subreddit in self.nsfw_subreddits:
                if self.nsfw_subreddits[str_subreddit] is True:
                    pass
                else:
                    non_nsfw_posts.append(post)
            else:
                is_nsfw = subreddit.over18
                self.nsfw_subreddits[str_subreddit] = is_nsfw
                if is_nsfw is True:
                    pass
                else:
                    non_nsfw_posts.append(post)

        return non_nsfw_posts
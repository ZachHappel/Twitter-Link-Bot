import mysql.connector
import praw
import time
class DB_Main:

    redditBot = praw.Reddit('bot1')


    def __init__(self, host, user, password):
        self.database = mysql.connector.connect(host = host, user = user, password = password)
        self.database_cursor = self.database.cursor(buffered=True)
        self.database_cursor.execute("USE db;")
        print("MySQL server initialized on database: db")


    def executeQuery(self, query_string):
        try:
            self.database_cursor.execute(query_string)
            print("Successfully completed")
            return True
        except Exception as e:
            print("Error occured when submitting query: " +str(e))
            return False


    def singularQueryRemoveNSFWSubreddits(self, submissions_found):
        non_nsfw_posts = []

        for post in submissions_found:
            content_link = post[0]
            reddit_link = post[1]
            subreddit = post[1].subreddit
            str_subreddit = str(subreddit)

            if str_subreddit[0:2] == 'u_':
                pass
            else:
                is_nsfw = self.isNSFW(str_subreddit)
                if is_nsfw is True:
                    pass
                else:
                    non_nsfw_posts.append((content_link, reddit_link, subreddit))

        return non_nsfw_posts

    def archiveURLsAndPosts(self, submissions):
        rows_appended = 0
        sql_b = "INSERT INTO Submissions(RedditURL, ContentURL, Subreddit, Tweet) VALUES"
        for submission in submissions:
            content_link = submission[0]
            reddit_link = submission[1].permalink
            subreddit = str(submission[2])
            is_tweet = str(submission[3])

            print("Content Link: "+str(content_link))
            print("Reddit Link: "+str(reddit_link))
            print("Subreddit: "+str(subreddit))
            print("Is Tweet: "+str(is_tweet))

            sql_e = "(%s, %s, %s, %s), " % ("'" + reddit_link + "'", "'" + content_link + "'", "'" + subreddit + "'", is_tweet)
            sql_b = sql_b + sql_e

        sql_b = sql_b[:len(sql_b) - 2] + ";"


        tries = 0
        while tries <= 4:

            try:
                self.database_cursor.execute(sql_b)
                self.database.commit()
                rows_appended+= int(self.database_cursor.rowcount)
                print("Posts inserted on Submissions: " + str(rows_appended))
                return

            except Exception as e:
                tries+=1
                time.sleep(.5)
                print("Error occurred while DB Archiving: "+str(e))



    def batchQueryRemoveNSFWPosts(self, submissions_found):

        subreddits_in_submissions = []
        db_subreddits = []
        non_nsfw = []

        subreddit_query = "SELECT * FROM Subreddits WHERE SR_Name = '' "
        insert_query = "INSERT INTO Subreddits(SR_Name, IsNSFW) VALUES"

        non_nsfw_submission_tuples = []

        for post in submissions_found:
            print("This is post: "+str(post))
            subreddit = post[1].subreddit
            str_subreddit = str(subreddit)
            subreddit_query = subreddit_query + " OR SR_NAME = '" + str_subreddit + "'"
            subreddits_in_submissions.append(str_subreddit)
        subreddit_query = subreddit_query + ';'

        try:
            self.database_cursor.execute(subreddit_query)
            self.database.commit()
            results = self.database_cursor.fetchall()
        except Exception as e:
            print("Error while requesting subreddits from DB: "+str(e))
            unfiltered_posts_list = []
            for unfiltered_post in submissions_found:
                unfiltered_posts_list.append((unfiltered_post[0], unfiltered_post[1], unfiltered_post[1].subreddit))
            return unfiltered_posts_list

        for result in results:
            sr_name = result[0]
            db_subreddits.append(sr_name)
            if bool(result[1]) is True:
                non_nsfw.append(sr_name)

        for sub_subreddit in subreddits_in_submissions:
            if sub_subreddit not in db_subreddits:
                if self.redditBot.subreddit(sub_subreddit).over18 is True:
                    insert_query = insert_query + " ( %s, %s)" % (sub_subreddit, "1") + ', '
                else:
                    insert_query = insert_query + " ( %s, %s)" % (sub_subreddit, "0") + ', '
                    non_nsfw.append(sub_subreddit)

        for submission in submissions_found:
            print("Before err?")
            print("After Before Err, Submission: "+str(submission[1].subreddit))
            if str(submission[1].subreddit) in non_nsfw:
                non_nsfw_submission_tuples.append((submission[0], submission[1], submission[1].subreddit))
            else:
                pass

        try:
            self.database_cursor.execute(insert_query)
            self.database.commit()
            print("Subreddits appended to table 'Subreddits'")
            return non_nsfw_submission_tuples
        except Exception as e:
            print("Error while requesting subreddits from DB: " + str(e))
            unfiltered_posts_list = []
            for unfiltered_post in submissions_found:
                unfiltered_posts_list.append((unfiltered_post[0], unfiltered_post[1], unfiltered_post[1].subreddit))
            return unfiltered_posts_list


    def isNSFW(self, subreddit_name):
        subreddits_added = 0
        self.executeQuery("SELECT IsNSFW FROM Subreddits WHERE SR_Name = '"+subreddit_name+"';")
        result = self.database_cursor.fetchall()

        if len(result) == 0:
            print("No results found for Subreddit: "+subreddit_name)
            nsfw = self.redditBot.subreddit(subreddit_name).over18

            if nsfw is True: bit_boolean = 1
            else: bit_boolean = 0

            sql = "INSERT INTO Subreddits(SR_Name, IsNSFW) VALUES( %s, %s)"
            vals = (subreddit_name, bit_boolean)

            self.database_cursor.execute(sql,vals)
            self.database.commit()
            print("Insertion made on table Subreddits")
            subreddits_added += int(self.database_cursor.rowcount)

            if bit_boolean == 1:
                return True
            else:
                return False

        else:
            print("Subreddit found")
            result = result[0][0]
            if int(result) == 1: return True
            else: return False

        print("Subreddits inserted on Subreddit: "+str(subreddits_added))



    def format(self, submissions_found):
        to_return = []
        for post in submissions_found:
            to_return.append((post[0], post[1], post[1].subreddit))

        return to_return
from clients import TwitterConnection
import json
import tweepy
import sys
from local_logging import Logging
from datetime import datetime
import time
from time_difference import time_diff


class Twitter_Main:

    tweet_archive = {}
    logging = Logging()
   # wave_obj = sa.WaveObject.from_wave_file("bell-ringing-04.wav")


    def __init__(self, client_id, client_secret, access_token_key, access_token_secret):
        self.TwitterBot = TwitterConnection(client_id, client_secret, access_token_key, access_token_secret).TwitterClientConnection
        self.TweepyAPI = TwitterConnection(client_id, client_secret, access_token_key, access_token_secret).TweepyAPIConnection
        self.archiveTimeStart()

    def archiveTimeStart(self):
        print("Time Start ")
        self.start = datetime.now()
        self.str_start = str(self.start)[:len(str(self.start)) - 7]
        self.formatted_str_start = datetime.strptime(self.str_start, '%Y-%m-%d %H:%M:%S')

    def archiveTimeCheck(self): # Clears tweet archive if archive is older than thirty minutes
        print("Time Check")
        self.end = datetime.now()
        self.str_end = str(self.end)[:len(str(self.end)) - 7]
        self.formatted_str_end = datetime.strptime(self.str_end, '%Y-%m-%d %H:%M:%S')
        self.time_diff = str(time_diff(self.formatted_str_start, self.formatted_str_end))
        self.time_diff_formatted = self.time_diff[3:4] + self.time_diff[5:]
        print("Time Difference: "+ self.time_diff_formatted)
        self.int_time_diff = int(self.time_diff_formatted)

        if self.int_time_diff >= 30:
            self.tweet_archive.clear()
            self.archiveTimeStart()
        else:
            pass


    def usernameTweetCombos(self, username_combos, tweet_combos):

        userTweet_combos = []

        for username in username_combos:
            for tweet in tweet_combos:
                userTweet_combos.append((username,tweet))

        return userTweet_combos

    #Future addition:
    #Keep archive of tweets for an hour, in the case that the same user is requested. Refresh once requested after an hour.



    def tweepyCycleCombinations(self, combinations):  #Creates combination of the variations made for username
                                                                        # and tweet body; passing them along to tweepySearch

        print("Testing Combinations...")
        print("Amount of Combinations: "+ str(len(combinations)))

        self.archiveTimeCheck()   # Checks to see if the archive is outdated prior to testing combinations
        for y in range(0, 2):
            for x in range(0, len(combinations)):
                if y == 0:
                    print(combinations[x][0])
                elif y == 1:
                    print(combinations[x][1])



        for x in range(0, len(combinations)):
            #selected_tuple = combinations[len(combinations) - 1 -x]
            tweet_body = combinations[len(combinations) - 1 -x][1] #Cascade list in reverse
            username = combinations[x][0]
            #username = selected_tuple[0]
            #tweet_body = selected_tuple[1]
            try:
                print('---------------------------')
                print('Combination '+str(x))
                print('')
                print("Term variation: "+tweet_body)
                print("Len tvariation: " + str(len(tweet_body)))
                print("Username var  : "+username)
                print('')
                print('---------------------------')
                response = self.tweepyPreSearch(tweet_body.split(), username)
            except ValueError as e:
                self.logging.error_log(e)
                continue
                #return None
            if response is None:
                print("** Nothing Found; Trying Different URL **")
                continue
                #return None
            else:
                print("Found")
                print(response)
                return response

        return None




    def tweepyPreSearch(self, terms, username):
        if username in self.tweet_archive:
            print("Reading tweets from user '" + username +"' in Tweet Archive...")
            response = self.tweepyArchiveSearch(terms, username, self.tweet_archive[username])
            return response
        else:
            response = self.tweepyNonArchiveSearch(terms, username)
            return response




    def tweepyArchiveSearch(self, terms, username, archived_tweets):
        response = self.parseTweepyTweetBatch(archived_tweets, terms, username)
        return response

    def tweepyNonArchiveSearch(self, terms, username):
        # Greatly expanding on Yanofsky's searching method
        # https://gist.github.com/yanofsky/5436496

        try:

            all_tweets = []
            new_tweets = self.TweepyAPI.user_timeline(screen_name=username, count=200)   #Initial search of tweets
            all_tweets.extend(new_tweets)                                               #Add new tweets to located tweets

            oldest = all_tweets[-1].id - 1

            outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in new_tweets]

            parseResults = self.parseTweepyTweetBatch(outtweets, terms, username)
            print("...%s tweets downloaded so far" % (len(all_tweets)))

            if parseResults is None: pass
            else: return parseResults

            while len(new_tweets) > 0:
                print("getting tweets before %s" % (oldest))
                new_tweets = self.TweepyAPI.user_timeline(screen_name=username, count=200, max_id=oldest)
                all_tweets.extend(new_tweets)
                self.tweet_archive[username] = all_tweets
                oldest = all_tweets[-1].id - 1
                print("...%s tweets downloaded so far" % (len(all_tweets)))
                outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in new_tweets]
                parseResults = self.parseTweepyTweetBatch(outtweets, terms, username)
                if parseResults is None: continue
                else: return parseResults

            return None

        except Exception as e:
            print("Error while getting Tweets: "+str(e))
            return None



    def parseTweepyTweetBatch(self, new_tweets, terms, username):

        print("Testing Batch...")
        amount_of_terms = len(terms)
        print(amount_of_terms)

        for x in range(0, len(new_tweets)):

            term_match_count = 0
            tweet_list = new_tweets[x]
            tweet_text = tweet_list[2]
            tweet_id = tweet_list[0]
            tweet_time = tweet_list[1]

            print("Tweet Text: "+tweet_text)

            splitted_tweet_text = tweet_text.split()
            matched_terms = ''
            print("Terms: " + str(terms))

            for term in terms:
                if term in splitted_tweet_text:
                    term_match_count+=1
                    matched_terms = matched_terms+term+" "

                if len(terms) == 2 and matched_terms == 2 and len(splitted_tweet_text) == 2:
                    print("#######################################################")
                    print ("                      Tweet Found!! [A] \n")
                    print("    Terms Matched: " + matched_terms)
                    print("Tweet In Question: " + tweet_text)
                    print("         Username:" + username)
                    print("#######################################################")
                    time.sleep(5)
                    #self.tweet_archive.clear()  # Remove!
                    return 'http://twitter.com/' + username + '/status/' + str(tweet_id)


                #in case of tweet ending in something similar to: "peaky blinders for h… https://t.co/694WSEtjQA"
                if 'http' in splitted_tweet_text[len(splitted_tweet_text)-1] and "…" in splitted_tweet_text[len(splitted_tweet_text)-2]:
                    if term_match_count == len(splitted_tweet_text) - 3 and term_match_count > 0:

                        print("#######################################################")
                        print ("                      Tweet Found!! [B] \n")
                        print("    Terms Matched: "+matched_terms)
                        print("Tweet In Question: "+tweet_text)
                        print("         Username:" +username)
                        print("#######################################################")
                        time.sleep(5)
                        #self.tweet_archive.clear()  # Remove!
                        return 'http://twitter.com/' + username + '/status/' + str(tweet_id)


                if (term_match_count == amount_of_terms and term_match_count >= 4)  or (term_match_count == amount_of_terms - 1 and term_match_count >= 4):
                    print("#######################################################")
                    print ("                      Tweet Found!! [C] \n")
                    print("    Terms Matched: " + matched_terms)
                    print("Terms Match Count: " + str(term_match_count))
                    print("Tweet In Question: " + tweet_text)
                    print("         Username:" + username)
                    print("#######################################################")
                    #play_obj = self.wave_obj.play()
                    #play_obj.wait_done()
                    time.sleep(5)
                    #self.tweet_archive.clear()  # Remove!
                    return 'http://twitter.com/' + username + '/status/' + str(tweet_id)
                else:
                    continue
        #self.tweet_archive.clear()   #Remove!
        return None


    def checktweetArchive(self, username):

        if username in self.tweet_archive:
            print(self.tweet_archive[username][0])
            return True
        else: return False












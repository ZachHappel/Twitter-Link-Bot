from clients import TwitterConnection
import json
import tweepy
from datetime import datetime
import sys
import time
from local_logging import Logging
#import simpleaudio as sa


class Twitter_Main:

    tweet_archive = {}
    logging = Logging
   # wave_obj = sa.WaveObject.from_wave_file("bell-ringing-04.wav")


    def __init__(self, client_id, client_secret, access_token_key, access_token_secret):
        self.TwitterBot = TwitterConnection(client_id, client_secret, access_token_key, access_token_secret).TwitterClientConnection
        self.TweepyAPI = TwitterConnection(client_id, client_secret, access_token_key, access_token_secret).TweepyAPIConnection


    def create_query(self, username, tweet_line):
        query_string = 'q='
        splitted_tweet_line = tweet_line.split(' ')

        #print("This is before query: " +str(splitted_tweet_line))

        for words in range(0, len(splitted_tweet_line)):
            words_to_add = splitted_tweet_line[words] + '%20'
            query_string += words_to_add


        #print("This is after creation: "+query_string)
        if '@' in username:
            query_string = query_string + 'from%3A' + username[1:]
        else:
            query_string = query_string + 'from%3A' + username

        newQueryString = ''
        for searching in range(0, len(query_string)):
            if query_string[searching] == '@':
                newQueryString = newQueryString + '%40'
            else:
                newQueryString = newQueryString + str(query_string[searching])

        print(newQueryString)
        return newQueryString


    def execute_search_queries(self, queries):

        for query_and_user in range(0, len(queries)):

            print("Here")

            selected_query_tuple = queries[0]
            query = selected_query_tuple[0]
            username = selected_query_tuple[1]

            print("Testing Query: "+str(query))
            results = self.TwitterBot.GetSearch(raw_query=query)

            if len(results) > 0:
                print("Tweet Found!")
                print("These are the results: " + str(results))
                found_tweet = results[0]
                json_str = json.dumps(found_tweet._json)
                id_tag = json_str.index('"id":')
                begin_of_id_index = id_tag + 6
                id = json_str[begin_of_id_index:begin_of_id_index + 18]
                found_tweet_url = 'http://twitter.com/' + username + '/status/' + str(id)
                if username == '':
                    print('Blank Username')
                    pass
                else:
                    return found_tweet_url

            if query_and_user == len(queries)-1:
                return None



    def execute_single_query(self, q, username):
        results = self.TwitterBot.GetSearch(raw_query=q)
        if len(results) > 0:
            print("Tweet Found!")
            print("These are the results: " + str(results))
            found_tweet = results[0]
            json_str = json.dumps(found_tweet._json)
            id_tag = json_str.index('"id":')
            begin_of_id_index = id_tag + 6
            id = json_str[begin_of_id_index:begin_of_id_index + 18]
            found_tweet_url = 'http://twitter.com/' + username + '/status/' + str(id)
            if username == '':
                print('Blank Username')
                pass
            else:
                print(found_tweet_url)
        else:
            print(results)



    def createQueries(self, username_combos, tweet_combos):
        queries = []
        for username in username_combos:
            for tweet in tweet_combos:
                queries.append( (self.create_query(username, tweet), username) )
        return queries


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
        for x in range(0, len(combinations)):
            selected_tuple = combinations[x]
            username = selected_tuple[0]
            tweet_body = selected_tuple[1]
            try:
                print('---------------------------')
                print('Combination '+str(x))
                print('')
                print("Term variation: "+tweet_body)
                print("Username var  : "+username)
                print('')
                print('---------------------------')
                response = self.tweepyPreSearch(tweet_body.split(), username)
            except ValueError as e:
                self.logging.error_log(e)
                return None
            if response is None:
                print("** Nothing Found; Trying Different URL **")
                return None
            else:
                print("Found")
                print(response)
                return response
        return None




    def tweepyPreSearch(self, terms, username):


        if username in self.tweet_archive:

            response = self.tweepyArchiveSearch(terms, username, self.tweet_archive[username])
            return response

        else:

            response = self.tweepyNonArchiveSearch(terms, username)
            return response




    def tweepyArchiveSearch(self, terms, username, archived_tweets):
        response = self.parseTweepyTweetBatch(archived_tweets, terms, username)
        return response


                                                                                        # Expanding on Yanofsky's searching method
    def tweepyNonArchiveSearch(self, terms, username):                                                # https://gist.github.com/yanofsky/5436496

        all_tweets = []
        new_tweets = self.TweepyAPI.user_timeline(screen_name=username, count=200)   #Initial search of tweets
        all_tweets.extend(new_tweets)                                               #Add new tweets to located tweets

        oldest = all_tweets[-1].id - 1

        outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in new_tweets]

        parseResults = self.parseTweepyTweetBatch(outtweets, terms, username)
        if parseResults is None: pass
        else: return parseResults

        while len(new_tweets) > 0:
            print("getting tweets before %s" % (oldest))
            new_tweets = self.TweepyAPI.user_timeline(screen_name=username, count=200, max_id=oldest)
            all_tweets.extend(new_tweets)
            oldest = all_tweets[-1].id - 1
            print("...%s tweets downloaded so far" % (len(all_tweets)))

            outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in new_tweets]
            parseResults = self.parseTweepyTweetBatch(outtweets, terms, username)
            if parseResults is None: continue
            else: return parseResults

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

            splitted_tweet_text = tweet_text.split()
            matched_terms = ''
            for y in range(0, len(terms)):

                term = terms[y]


                if term in tweet_text:
                    term_match_count+=1
                    matched_terms = matched_terms+" "+matched_terms

                if len(terms) == 2 and matched_terms == 2 and len(splitted_tweet_text) == 2:
                    print("#######################################################")
                    print ("                      Tweet Found!! [A] \n")
                    print("    Terms Matched: " + matched_terms)
                    print("Tweet In Question: " + tweet_text)
                    print("         Username:" + username)
                    print("#######################################################")
                    time.sleep(1)
                    return 'http://twitter.com/' + username + '/status/' + str(tweet_id)




                #in case of tweet ending in "peaky blinders for h… https://t.co/694WSEtjQA"
                if 'http' in splitted_tweet_text[len(splitted_tweet_text)-1] and "…" in splitted_tweet_text[len(splitted_tweet_text)-2]:
                    if term_match_count == len(splitted_tweet_text) - 3:

                        print("#######################################################")
                        print ("                      Tweet Found!! [A] \n")
                        print("    Terms Matched: "+matched_terms)
                        print("Tweet In Question: "+tweet_text)
                        print("         Username:" +username)
                        print("#######################################################")
                        time.sleep(1)
                        return 'http://twitter.com/' + username + '/status/' + str(tweet_id)


                if term_match_count == amount_of_terms -1:
                    print("#######################################################")
                    print ("                      Tweet Found!! [B] \n")
                    print("    Terms Matched: " + matched_terms)
                    print("Tweet In Question: " + tweet_text)
                    print("         Username:" + username)
                    print("#######################################################")
                    #play_obj = self.wave_obj.play()
                    #play_obj.wait_done()
                    time.sleep(1)
                    return 'http://twitter.com/' + username + '/status/' + str(tweet_id)
                else:
                    continue

        return None




    def checktweetArchive(self, username):

        if username in self.tweet_archive:
            print(self.tweet_archive[username][0])
            return True
        else: return False





from __future__ import unicode_literals
import twitter
import json
from newTweepy import tweepySearch, parse_tweepy_response


# found_tweet = (results[0])
# json_str = json.dumps(found_tweet._json)
# print(json_str.index('"id":'))
# print(len('950826688732155904'))
# tweet = (results[0])
# print(tweet)







def find_tweet(username_combos, tweet_combos):
    def create_query(username, firstline):
        print("this is first line: " + firstline)
        query_string = 'q='
        splitted_line = firstline.split(' ')
        print("this is splitted line: " + str(splitted_line))

        for words in range(0, len(splitted_line)):
            query_string = query_string + (splitted_line[words]) + '%20'

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
        print("HERE")
        print(newQueryString)
        return newQueryString

    def cycle_combinations(username_combos, tweet_combos):

        consumer_key = [""]
        consumer_secret = [""]

        access_token_key = [""]
        access_token_secret = [""]

        api = twitter.Api(consumer_key[0],
                          consumer_secret[0],
                          access_token_key[0],
                          access_token_secret[0], sleep_on_rate_limit=True)

        for usernames in range(0, len(username_combos)):

            for tweets in range(0, len(tweet_combos)):

                try:
                    print("Username: " + str(username_combos[usernames] + ", \n"
                                                                          "Tweet: " + (tweet_combos[tweets]).encode(
                        'utf-8')))  # !!!!

                    #query = create_query(username_combos[usernames], tweet_combos[tweets])
                    #results = api.GetSearch(raw_query=query)

                    usernameUsedForSearch = username_combos[usernames]  # Needed to compile final URL
                    tweetUsedForSearch = tweet_combos[tweets]

                    tweepy_search_results = tweepySearch(usernameUsedForSearch)
                    parse_results = parse_tweepy_response(usernameUsedForSearch, tweepy_search_results,
                                                          tweetUsedForSearch)
                    if parse_results == 'Tweepy Search Results: None':
                        query = create_query(username_combos[usernames], tweet_combos[tweets])
                        results = api.GetSearch(raw_query=query)
                        if len(results) > 0:
                            print("Tweet Found!")
                            print("These are the results: " + str(results))
                            found_tweet = results[0]
                            json_str = json.dumps(found_tweet._json)
                            id_tag = json_str.index('"id":')
                            begin_of_id_index = id_tag + 6
                            id = json_str[begin_of_id_index:begin_of_id_index + 18]
                            found_tweet_url = 'http://twitter.com/' + usernameUsedForSearch + '/status/' + str(id)
                            if usernameUsedForSearch == '':
                                print('Blank Username')
                                pass
                            else:
                                return found_tweet_url
                        else:
                            return("Tweepy Search Results: None")

                    else:
                        return parse_results  # URL



                except:
                    break

    return (cycle_combinations(username_combos, tweet_combos))















    # find_tweet(['Woody-See', 'WoodySee', 'Woody_See'], ['did u really short me a gram bro let me', 'did u really me a gram bro let me', 'did u really short me a gram bro me'])
    # print(tweet['find'])
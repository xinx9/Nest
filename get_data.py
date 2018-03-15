# Megan Ramaker
#
# Relation Bot
#
# EHacks2018

def get_user_Name():
    username = input("Enter a username:")
    type(username)

    return username

def get_followers(username):
    followers = []
    for page in tweepy.Cursor(api.followers_ids, screen_name=username, count=5000).pages():
     followers.extend(page)
     #print(followers)
     time.sleep(4)

    #  with open ("followers.csv", 'wb') as outFile:
    #      wr = csv.writer(outFile, dialect = 'excel')
    #      wr.writerows(followers)

     return followers


def get_followed(username):
    friends = []
    for page in tweepy.Cursor(api.friends_ids, screen_name=username, count = 5000).pages():
        friends.extend(page)
        #print(friends)
        time.sleep(4)

        # for result in result_list:
        #     row.append(result.getvalue())

        # with open ("friends.csv", 'wb') as outFile:
        #  wr = csv.writer(outFile, dialect = 'excel')
        #  wr.writerows(friends)

    return friends

def find_retweets_ids():
    results = api.retweets()

def compare_lists(followers, friends):
    results = set(followers).intersection(friends)
    print (results)


##### Main ######

import tweepy
import time
import csv
import csv

consumer_key = 'xA0UUTUy4bgomAIW8mEQiMfdO'
consumer_secret = 'PcaSyhiejX5Pf9SV88WuiRagG0adffqdA1WZy4p4Oz3kwwVXj0'
access_token = '969729457996038145-gsxZ5uH3o7A7sTyav6dgYWKtB2rs4GO'
access_token_secret = 'TJSszVySD1dlobHWGNsGRGSv8fBCJkkJ5dclgOFvjwoZ5'

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

if __name__ == "__main__":
    username = get_user_Name()

    followers = get_followers(username)

    friends = get_followed(username)

    compare_lists(followers, friends)

    user = api.get_user("m4delynne")
    print(user._json)


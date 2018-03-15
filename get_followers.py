# Megan Ramaker
#
# Relation Bot
#
# EHacks2018

import csv
import tweepy
from time import sleep
from credentials import *

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth) 

screen_name = 'm4delynne'
file_name = "followers_data/follower_ids-" + screen_name + ".txt"
with open(file_name) as f:
    ids = [x.strip() for x in f.readlines()]

num_samples = 30
friends = dict()

# Initialise i
i = 0

# We want to check that i is less than our number of samples, but we also need to make
# sure there are IDs left to choose from.
while i <= num_samples and ids:
    current_id = random.choice(ids)

    # remove the ID we're testing from the list, so we don't pick it again.
    ids.remove(current_id)

    try:
        # try to get friends, and add them to our dictionary value if we can
        # use .get() to cope with the first loop.
        for page in tweepy.Cursor(api.friends_ids, current_id).pages():
            friends[current_id] = friends.get(current_id, []) + page
        i += 1
    except tweepy.TweepError:
        # we get a tweep error when we can't view a user - skip them and move onto the next.
        # don't increment i as we want to replace this user with someone else.
        print 'Could not view user {}, skipping...'.format(current_id)

def id_to_name(id):
    user = api.get_user(id)
    return user.screen_name
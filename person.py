import csv
import tweepy
from time import sleep
from get_data import *
import pickle

# TODO:
# Create a function to check the available API keys and switch to the best one

class People:
    people = []
    target = None
    recursion_depth = 5 # People deep
    api_cooldown = 4 # seconds
    API_KEY = ['uDlkgFCnpbZQ6yqweBFLk6tTL', 'eeVdzC9gpwc6Uk1APuwz4Z68I']
    API_SECRET = ['giwwjxKnGmVrCvodZlcuJd2YDzzEvQsOb9OMOjQtf69qpHdhhd', 'R7jj2F7UkfoKTVaDIPbNCImhKTGpkZx448YCzDA2vhYto0EXHn']
    auth = None
    api = None
    followee_requests_left_on_key = 0
    follower_requests_left_on_key = 0
    rate_limit_remaining = 0

    @classmethod
    def get_person_by_id(self, id):
        for i in People.people:
            if i.tw_id == id:
                return i
    
    @classmethod
    def set_target_by_uname(self, uname):
        user = self.api.get_user(uname)
        self.target = PersonNode(user.id)

    @classmethod
    def reset_auth_and_key(self, key_index):
        self.auth = tweepy.AppAuthHandler(self.API_KEY[key_index], self.API_SECRET[key_index])
        self.api = tweepy.API(auth, wait_on_rate_limit=True,
                         wait_on_rate_limit_notify=True)
        self.update_requests()
        self.get_api_limit_remaing()

    @classmethod
    def update_requests(self):
        data = self.api.rate_limit_status()
        self.follower_requests_left_on_key = data['resources']['followers']['/followers/ids']['remaining']
        self.followee_requests_left_on_key = data['resources']['friends']['/friends/ids']['remaining']

    @classmethod
    def get_api_limit_remaing(self):
        data = self.api.rate_limit_status()
        self.rate_limit_remaining = data['resources']['application']['/application/rate_limit_status']['remaining']
        return self.rate_limit_remaining

    @classmethod
    def save_object(obj, filename):
        with open(filename, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


class PersonNode(People):

    def get_screenname_from_id(self):
        if self.userObj != None:
            self.screenName = self.userObj.screen_name

    def get_followers(self):  # Returns a list of follower IDs
        followers = []
        for page in tweepy.Cursor(api.followers_ids, screen_name=self.screenName).pages():
            followers.extend(page)
            #data = self.api.rate_limit_status()
            #self.update_requests()
            #print("Followers get: {}/15 remaining".format(data['resources']['followers']['/followers/ids']['remaining']))
            time.sleep(self.api_cooldown)

        return followers

    def get_followees(self):  # Returns a list of followees IDs
        followees = []
        for page in tweepy.Cursor(api.friends_ids, screen_name=self.screenName, count=5000).pages():
            followees.extend(page)
            #data = self.api.rate_limit_status()
            #self.update_requests()
            #print("Friends/Followees get: {}/15 remaining".format(data['resources']['friends']['/friends/ids']['remaining']))
            time.sleep(self.api_cooldown)

        return followees

    def set_edges(self):  # Gets mutual followers&followees, creates and returns a list of them
        #  And sets self.edges to a list of people from the returned IDs
        self.followees = self.get_followees()
        self.followers = self.get_followers()

        mutual = set(self.followers).intersection(self.followees)
        self.numMutual = len(mutual)

        count = 0
        for user_id in mutual:
            try:
                tmp_pNode = PersonNode(user_id)
                print("GOT: @{}\t{}/{}".format(tmp_pNode.screenName, count, len(mutual)))
                self.edges.append(tmp_pNode)
                self.people.append(tmp_pNode)
                count += 1
            except tweepy.error.TweepError:
                print("User is private")
        return mutual

    def __init__(self, tw_id):  # Constructor
        self.tw_id = tw_id
        self.userObj = api.get_user(tw_id)
        self.get_screenname_from_id()
        self.numFollowees = self.userObj.friends_count
        self.numFollowers = self.userObj.followers_count
        self.edges = []
        self.numMutual = 0
        sleep(1);
    



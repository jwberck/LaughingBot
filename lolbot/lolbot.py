
import praw
import pdb
import re
import os
from config_lolbot import *


USER_AGENT = ("LaughingBot 0.1")

MESSAGE = "lol"

r = praw.Reddit(USER_AGENT)

subreddit = r.get_subreddit("me_irl")

for submission in subreddit.get_hot(limit = 5):
    print("Title: ", submission.title)
    print("Text: ", submission.selftext)
    print("Score ", submission.score)
    print("-----------------------------\n")

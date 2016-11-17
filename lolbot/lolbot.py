
import praw
import pdb
import re
import os
from config_lolbot import *


if not os.path.isfile("config_lolbot.py"):
    print("No valid config file found")
    exit(1)

USER_AGENT = ("LaughingBot 0.1")

MESSAGE = "lol"

r = praw.Reddit(USER_AGENT)

r.login(REDDIT_USERNAME, REDDIT_PASS)

if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = filter(None, posts_replied_to)

subreddit = r.get_subreddit("pythonforengineers")

for comment in r.get_comments("pythonforengineers"):
    body = comment.body.lower()
    if re.search("lol", body, re.IGNORECASE) and comment.score < -1 and comment.id not in posts_replied_to:
        comment.reply(MESSAGE)
        posts_replied_to.add(comment.id)
        print("Comment Made!")



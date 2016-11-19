
import praw
import re
import os
from config_lolbot import app_key, app_secret, access_token, refresh_token
from settings import USER_AGENT, scopes
from prawoauth2 import PrawOAuth2Mini


if not os.path.isfile("config_lolbot.py"):
    print("No valid config file found")
    exit(1)

MESSAGE = "lol"

r = praw.Reddit(USER_AGENT)

oauth_helper = PrawOAuth2Mini(r, app_key=app_key,
                              app_secret=app_secret, access_token=access_token,
                              scopes=scopes, refresh_token=refresh_token)

#gets the posts_replied_to file
if not os.path.isfile("posts_replied_to.txt"):
     posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = filter(None, posts_replied_to)

#defines main functionality of lolbot
def lolbot_loop():
    oauth_helper.refresh()
    for comment in r.get_comments("pythonforengineers"):
        body = comment.body.lower()
        if re.search("lol", body, re.IGNORECASE) and comment.score < 5 and comment.id not in posts_replied_to:
            comment.reply(MESSAGE)
            posts_replied_to.add(comment.id)
            print("Comment Made!")
            exit(1)

#handles Oauth refreshing
while True:
    try:
        lolbot_loop()
    except praw.errors.OAuthInvalidToken:
        oauth_helper.refresh()

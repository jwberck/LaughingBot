
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

#defines main functionality of lolbot
def lolbot_loop(comments, posts_replied_to):

    for comment in comments:
        body = comment.body.lower()
        if re.search("python", body, re.IGNORECASE) and comment.score < 5 and comment.id not in posts_replied_to:
            print("made it into if")
            comment.reply(MESSAGE)
            print("made it past reply")
            posts_replied_to.append(comment.id)
            print("Comment added to posts_replied_to.txt!")
            exit(1)

#gets the posts_replied_to file
if not os.path.isfile("posts_replied_to.txt"):
     posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = filter(None, posts_replied_to)



#handles Oauth refreshing
while True:
    try:
        comments = r.get_comments("pythonforengineers")
        lolbot_loop(comments, posts_replied_to)
    except praw.errors.OAuthInvalidToken:
        oauth_helper.refresh()

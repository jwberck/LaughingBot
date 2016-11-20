
import praw
import re
import os
from config_lolbot import app_key, app_secret, access_token, refresh_token
from settings import USER_AGENT, scopes
from prawoauth2 import PrawOAuth2Mini


# defines main functionality of lolbot
def lolbot_loop(comments, posts_replied_to):
    MESSAGE = "lol"
    for comment in comments:

        author = comment.author.name

        if author == "LaughingBot":
            print("found author")
            continue

        body = comment.body.lower()
        if re.search("HARAMBAE", body, re.IGNORECASE) and comment.score < 10 and comment.id not in posts_replied_to:
            print("made it into if")
            comment.reply(MESSAGE)
            print("made it past reply")
            posts_replied_to.append(comment.id)
            print("Comment added to posts_replied_to")
            # Write our updated list back to the file
            with open("posts_replied_to.txt", "w") as f:
                for post_id in reddit_posts_replied_to:
                    f.write(post_id + "\n")
            print("updated posts_replied_to written to file")
            exit(1)



if not os.path.isfile("config_lolbot.py"):
    print("No valid config file found")
    exit(1)

reddit_instance = praw.Reddit(USER_AGENT)
oauth_helper = PrawOAuth2Mini(reddit_instance, app_key=app_key,
                              app_secret=app_secret, access_token=access_token,
                              scopes=scopes, refresh_token=refresh_token)

# gets the posts_replied_to file
if not os.path.isfile("posts_replied_to.txt"):
     reddit_posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
        reddit_posts_replied_to = f.read()
        reddit_posts_replied_to = reddit_posts_replied_to.split("\n")
        reddit_posts_replied_to = filter(None, reddit_posts_replied_to)

# handles Oauth refreshing
while True:
    try:
        reddit_comments = reddit_instance.get_comments("pythonforengineers")
        lolbot_loop(reddit_comments, reddit_posts_replied_to)
    except praw.errors.OAuthInvalidToken:
        oauth_helper.refresh()



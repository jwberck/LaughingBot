
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

        # prevents bot from responding to its self
        if author == "LaughingBot":
            print("found author")
            continue

        if comment.score < -5:
            print(comment.author)
            print(comment.score)
            print(comment.body)


        # searches a subreddit for the phrase "lol". if it is downvoted enough, it will respond with "lol"
        body = comment.body.lower()
        if re.search("lol", body, re.IGNORECASE) and comment.score < -10 and comment.id not in posts_replied_to:
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
        print("in high level loop")
        subreddit = reddit_instance.get_subreddit("me_irl")
        reddit_comments = subreddit.get_comments(limit=None)
        lolbot_loop(reddit_comments, reddit_posts_replied_to)
    except praw.errors.OAuthInvalidToken:
        oauth_helper.refresh()
        print("oauth refreshed")




import praw
import re
import os
from config_lolbot import app_key, app_secret, access_token, refresh_token
from settings import USER_AGENT, scopes
from prawoauth2 import PrawOAuth2Mini


# defines main functionality of lolbot
def lolbot_loop(submissions, posts_replied_to):
    message = "lol"

    submission_count = 0

    for submission in submissions:
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        comment_count = 0
        for comment in flat_comments:
            try:
                if comment.score < -5:
                    print(comment.author)
                    print(comment.score)
                    print(comment.body)
            except Exception:
                print("found more comment object")
                continue

            # searches a subreddit for the phrase "lol". if it is downvoted enough, it will respond with "lol"
            body = comment.body.lower()
            if re.search("lol", body, re.IGNORECASE) and comment.score < -10 and comment.id not in posts_replied_to:

                # prevents bot from responding to its self
                author = comment.author.name
                if author == "LaughingBot":
                    print("found author")
                    continue

                print("made it into if")
                comment.reply(message)
                print("made it past reply")
                posts_replied_to.append(comment.id)
                print("Comment added to posts_replied_to")
                # Write our updated list back to the file
                with open("posts_replied_to.txt", "w") as f:
                    for post_id in reddit_posts_replied_to:
                        f.write(post_id + "\n")
                print("updated posts_replied_to written to file")
                exit(1)
            comment_count += 1
            print("Comment Count: {}".format(comment_count))
        submission_count += 1
        print("Submission count: {}".format(submission_count))
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
    with open("posts_replied_to.txt", "r") as p:
        reddit_posts_replied_to = p.read()
        reddit_posts_replied_to = reddit_posts_replied_to.split("\n")
        reddit_posts_replied_to = filter(None, reddit_posts_replied_to)

# handles Oauth refreshing
while True:
    try:
        print("in high level loop")
        subreddit = reddit_instance.get_subreddit("me_irl")
        print("got reddit instance")
        reddit_submissions = subreddit.get_hot(limit=1024)
        print("got reddit submissions")
        lolbot_loop(reddit_submissions, reddit_posts_replied_to)
    except praw.errors.OAuthInvalidToken:
        oauth_helper.refresh()
        print("oauth refreshed")



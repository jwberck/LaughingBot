
import praw
from prawoauth2 import PrawOAuth2Server
from settings import USER_AGENT, scopes
from config_lolbot import *

r = praw.Reddit(USER_AGENT)

oauthserver = PrawOAuth2Server(r,app_key, app_secret, state=USER_AGENT, scopes= scopes)
oauthserver.start()

tokens = oauthserver.get_access_codes()
print(tokens)
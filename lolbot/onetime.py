
import praw
from prawoauth2 import PrawOAuth2Server
from settings import USER_AGENT, scopes

r = praw.Reddit(USER_AGENT)

oauthserver = PrawOAuth2Server(r,CLIENT_ID, CLIENT_SECRET, state=USER_AGENT, scopes= scopes)
oauthserver.start()

tokens = oauthserver.get_access_codes()
print(tokens)
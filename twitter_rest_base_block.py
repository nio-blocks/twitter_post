import requests
from requests_oauthlib import OAuth1
from nio.block.base import Block
from nio.properties.object import ObjectProperty
from nio.properties.holder import PropertyHolder
from nio.properties.string import StringProperty


VERIFY_CREDS_URL = ('https://api.twitter.com/1.1/'
                    'account/verify_credentials.json')


class TwitterCreds(PropertyHolder):

    """ Property holder for Twitter OAuth credentials.

    """
    consumer_key = StringProperty(title='API Key',
                                  default="[[TWITTER_API_KEY]]")
    app_secret = StringProperty(title='API Secret',
                                default="[[TWITTER_API_SECRET]]")
    oauth_token = StringProperty(title='Access Token',
                                 default="[[TWITTER_ACCESS_TOKEN]]")
    oauth_token_secret = \
        StringProperty(title='Access Token Secret',
                       default="[[TWITTER_ACCESS_TOKEN_SECRET]]")


class TwitterRestBase(Block):

    creds = ObjectProperty(TwitterCreds, title='Credentials')

    def __init__(self):
        super().__init__()
        self._auth = None

    def start(self):
        super().start()
        self._auth = self._authorize()

    def _authorize(self):
        """ Prepare the OAuth handshake and verify.

        """
        try:
            auth = OAuth1(self.creds().consumer_key(),
                          self.creds().app_secret(),
                          self.creds().oauth_token(),
                          self.creds().oauth_token_secret())
            resp = requests.get(VERIFY_CREDS_URL, auth=auth)
            if resp.status_code != 200:
                raise Exception("Status %s" % resp.status_code)
            return auth
        except Exception:
            self.logger.error("Authentication Failed "
                               "for consumer key: %s" %
                               self.creds().consumer_key())

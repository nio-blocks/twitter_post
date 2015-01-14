import requests
import json
from urllib.parse import quote
import oauth2 as oauth
from requests_oauthlib import OAuth1

from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties.object import ObjectProperty
from nio.metadata.properties.holder import PropertyHolder
from nio.metadata.properties.expression import ExpressionProperty
from nio.metadata.properties.string import StringProperty
from nio.modules.threading import Thread


VERIFY_CREDS_URL = ('https://api.twitter.com/1.1/'
                    'account/verify_credentials.json')
POST_URL = "https://api.twitter.com/1.1/statuses/update.json"


class TwitterCreds(PropertyHolder):

    """ Property holder for Twitter OAuth credentials.

    """
    consumer_key = StringProperty(title='Consumer Key')
    app_secret = StringProperty(title='App Secret')
    oauth_token = StringProperty(title='OAuth Token')
    oauth_token_secret = StringProperty(title='OAuth Token Secret')


@Discoverable(DiscoverableType.block)
class TwitterPost(Block):

    status = ExpressionProperty(default='', title='Status Update')
    creds = ObjectProperty(TwitterCreds, title='Credentials')

    def __init__(self):
        super().__init__()
        self._auth = None

    def start(self):
        super().start()
        self._auth = self._authorize()

    def process_signals(self, signals):
        for s in signals:
            try:
                status = self.status(s)
            except Exception as e:
                self._logger.error(
                    "Status evaluation failed: {0}: {1}".format(
                        type(e).__name__, str(e))
                )
                continue

            data = {'status': status}
            self._post_tweet(data)

    def _post_tweet(self, payload):
        response = requests.post(POST_URL, data=payload,
                                 auth=self._auth)

        status = response.status_code
        if status != 200:
            response = response.json()
            self._logger.error(
                "Twitter post failed with status {0}".format(status)
            )
            if 186 in [e.get('code') for e in response.get('errors')]:
                self._logger.error("Status is over 140 characters")
        else:
            self._logger.debug(
                "Posted '{0}' to Twitter!".format(payload['status'])
            )

    def _authorize(self):
        """ Prepare the OAuth handshake and verify.

        """
        try:
            auth = OAuth1(self.creds.consumer_key,
                          self.creds.app_secret,
                          self.creds.oauth_token,
                          self.creds.oauth_token_secret)
            resp = requests.get(VERIFY_CREDS_URL, auth=auth)
            if resp.status_code != 200:
                raise Exception("Status %s" % resp.status_code)
            return auth
        except Exception:
            self._logger.error("Authentication Failed "
                               "for consumer key: %s" %
                               self.creds.consumer_key)

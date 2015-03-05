import requests

from .twitter_rest_base_block import TwitterRestBase
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties import ExpressionProperty


VERIFY_CREDS_URL = ('https://api.twitter.com/1.1/'
                    'account/verify_credentials.json')
POST_URL = "https://api.twitter.com/1.1/statuses/update.json"


@Discoverable(DiscoverableType.block)
class TwitterPost(TwitterRestBase):

    status = ExpressionProperty(default='', title='Status Update')

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
            try:
                response = response.json()
                self._logger.error(
                    "Twitter post failed with status {0}".format(status)
                )
                if 186 in [e.get('code') for e in response.get('errors')]:
                    self._logger.error("Status is over 140 characters")
            except Exception as e:
                self._logger.error(
                    "Failed to process error response: {}: {}".format(
                        type(e).__name__, str(e)))
        else:
            self._logger.debug(
                "Posted '{0}' to Twitter!".format(payload['status'])
            )

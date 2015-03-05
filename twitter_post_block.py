import requests

from .twitter_rest_base_block import TwitterRestBase
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties import ExpressionProperty


POST_URL = "https://api.twitter.com/1.1/statuses/update.json"


@Discoverable(DiscoverableType.block)
class TwitterPost(TwitterRestBase):

    status = ExpressionProperty(default='', title='Status Update')

    def process_signals(self, signals):
        for s in signals:
            try:
                status = self.status(s)
            except Exception:
                self._logger.exception("Status evaluation failed")
                continue

            data = {'status': status}
            self._post_tweet(data)

    def _post_tweet(self, payload):
        response = requests.post(POST_URL, data=payload, auth=self._auth)

        status = response.status_code
        if status != 200:
            try:
                response = response.json()
                self._logger.error(
                    "Twitter post failed with status {0}".format(status)
                )
                if 186 in [e.get('code') for e in response.get('errors')]:
                    self._logger.error("Status is over 140 characters")
            except Exception:
                self._logger.exception("Failed to process error response")
        else:
            self._logger.debug(
                "Posted '{0}' to Twitter!".format(payload['status']))

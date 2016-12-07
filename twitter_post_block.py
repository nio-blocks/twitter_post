import requests

from .twitter_rest_base_block import TwitterRestBase
from nio.util.discovery import discoverable
from nio.properties import Property


POST_URL = "https://api.twitter.com/1.1/statuses/update.json"


@discoverable
class TwitterPost(TwitterRestBase):

    status = Property(default='', title='Status Update')

    def process_signals(self, signals):
        for s in signals:
            try:
                status = self.status(s)
            except Exception:
                self.logger.exception("Status evaluation failed")
                continue

            data = {'status': status}
            self._post_tweet(data)

    def _post_tweet(self, payload):
        response = requests.post(POST_URL, data=payload, auth=self._auth)

        status = response.status_code
        if status != 200:
            try:
                response = response.json()
                self.logger.error(
                    "Twitter post failed with status {0}".format(status)
                )
                if 186 in [e.get('code') for e in response.get('errors')]:
                    self.logger.error("Status is over 140 characters")
            except Exception:
                self.logger.exception("Failed to process error response")
        else:
            self.logger.debug(
                "Posted '{0}' to Twitter!".format(payload['status']))

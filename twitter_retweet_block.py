import requests
from .twitter_rest_base_block import TwitterRestBase
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties.expression import ExpressionProperty


POST_URL = "https://api.twitter.com/1.1/statuses/retweet/{}.json"


@Discoverable(DiscoverableType.block)
class TwitterRetweet(TwitterRestBase):

    id = ExpressionProperty(default='{{$id}}', title='Tweet ID')

    def process_signals(self, signals):
        for s in signals:
            try:
                id = self.id(s)
            except Exception as e:
                self._logger.error(
                    "ID evaluation failed: {0}: {1}".format(
                        type(e).__name__, str(e))
                )
                continue
            try:
                id = int(id)
            except Exception as e:
                self._logger.error(
                    "ID {} is not an integer: {}".format(id, e)
                )
                continue
            self._retweet_tweet(id)

    def _retweet_tweet(self, id):
        response = requests.post(POST_URL.format(id), auth=self._auth)
        status = response.status_code
        if status == 403:
            self._logger.error(
                "Twitter post failed with status {0}. "
                "Update limit has been hit.".format(status)
            )
        elif status != 200:
            self._logger.error(
                "Twitter post failed with status {0}".format(status)
            )
        else:
            self._logger.debug(
                "Retweeted tweet with id {}.".format(payload['id'])
            )

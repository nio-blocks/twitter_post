import requests
from .twitter_rest_base_block import TwitterRestBase
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties.expression import ExpressionProperty


POST_URL = "https://api.twitter.com/1.1/favorites/create.json"


@Discoverable(DiscoverableType.block)
class TwitterFavorite(TwitterRestBase):

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
            data = {'id': id}
            self._favorite_tweet(data)

    def _favorite_tweet(self, payload):
        response = requests.post(POST_URL, data=payload,
                                 auth=self._auth)
        status = response.status_code
        if status != 200:
            self._logger.error(
                "Twitter favorite {} failed with status {}".format(
                    payload['id'],
                    status
                )
            )
        else:
            self._logger.debug(
                "Favorited tweet with id {}.".format(payload['id'])
            )
from unittest.mock import patch, MagicMock
from ..twitter_favorite_block import TwitterFavorite
from nio.common.signal.base import Signal
from nio.util.support.block_test_case import NIOBlockTestCase


class TestTwitterFavorite(NIOBlockTestCase):

    @patch('twitter_rest.twitter_favorite_block.TwitterFavorite._authorize')
    @patch('twitter_rest.twitter_favorite_block.'
           'TwitterFavorite._favorite_tweet')
    def test_process_signal(self, mock_post, mock_auth):
        signals = [Signal({'id': 123})]
        blk = TwitterFavorite()
        self.configure_block(blk, {})
        blk.start()
        blk.process_signals(signals)
        mock_post.assert_called_once_with({'id': signals[0].id})
        blk.stop()

    @patch('twitter_rest.twitter_favorite_block.TwitterFavorite._authorize')
    @patch('twitter_rest.twitter_favorite_block.'
           'TwitterFavorite._favorite_tweet')
    def test_process_multiple(self, mock_post, mock_auth):
        signals = [
            Signal({'id': 123}),
            Signal({'id': 456}),
            Signal({'id': 789})
        ]
        blk = TwitterFavorite()
        self.configure_block(blk, {})
        blk.start()
        blk.process_signals(signals)
        self.assertEqual(mock_post.call_count, len(signals))
        blk.stop()

    @patch('twitter_rest.twitter_favorite_block.TwitterFavorite._authorize')
    @patch('twitter_rest.twitter_favorite_block.'
           'TwitterFavorite._favorite_tweet')
    def test_bad_config(self, mock_post, mock_auth):
        signals = [Signal({'id': 123})]
        blk = TwitterFavorite()
        self.configure_block(blk, {'id': '{{id+2}}'})
        blk._logger.error = MagicMock()
        blk.start()
        blk.process_signals(signals)
        self.assertEqual(blk._logger.error.call_count, 1)
        self.assertEqual(mock_post.call_count, 0)
        blk.stop()

    @patch('twitter_rest.twitter_favorite_block.TwitterFavorite._authorize')
    @patch('twitter_rest.twitter_favorite_block.'
           'TwitterFavorite._favorite_tweet')
    def test_bad_id(self, mock_post, mock_auth):
        signals = [Signal({'id': 'asdf'})]
        blk = TwitterFavorite()
        self.configure_block(blk, {})
        blk._logger.error = MagicMock()
        blk.start()
        blk.process_signals(signals)
        self.assertEqual(blk._logger.error.call_count, 1)
        self.assertEqual(mock_post.call_count, 0)
        blk.stop()

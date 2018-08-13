from unittest.mock import patch, MagicMock
from ..twitter_favorite_block import TwitterFavorite
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase


class TestTwitterFavorite(NIOBlockTestCase):

    @patch.object(TwitterFavorite, '_authorize')
    @patch.object(TwitterFavorite, '_favorite_tweet')
    def test_process_signal(self, mock_post, mock_auth):
        signals = [Signal({'tweet_id': 145})]
        blk = TwitterFavorite()
        self.configure_block(blk, {})
        blk.start()
        blk.process_signals(signals)
        mock_post.assert_called_once_with({'tweet_id': signals[0].tweet_id})
        blk.stop()

    @patch.object(TwitterFavorite, '_authorize')
    @patch.object(TwitterFavorite, '_favorite_tweet')
    def test_process_multiple(self, mock_post, mock_auth):
        signals = [
            Signal({'tweet_id': 123}),
            Signal({'tweet_id': 456}),
            Signal({'tweet_id': 789})
        ]
        blk = TwitterFavorite()
        self.configure_block(blk, {})
        blk.start()
        blk.process_signals(signals)
        self.assertEqual(mock_post.call_count, len(signals))
        blk.stop()

    @patch.object(TwitterFavorite, '_authorize')
    @patch.object(TwitterFavorite, '_favorite_tweet')
    def test_bad_config(self, mock_post, mock_auth):
        signals = [Signal({'tweet_id': 123})]
        blk = TwitterFavorite()
        self.configure_block(blk, {'tweet_id': '{{tweet_id+2}}'})
        blk.logger.error = MagicMock()
        blk.start()
        blk.process_signals(signals)
        self.assertEqual(blk.logger.error.call_count, 1)
        self.assertEqual(mock_post.call_count, 0)
        blk.stop()

    @patch.object(TwitterFavorite, '_authorize')
    @patch.object(TwitterFavorite, '_favorite_tweet')
    def test_bad_id(self, mock_post, mock_auth):
        signals = [Signal({'tweet_id': 'asdf'})]
        blk = TwitterFavorite()
        self.configure_block(blk, {})
        blk.logger.error = MagicMock()
        blk.start()
        blk.process_signals(signals)
        self.assertEqual(blk.logger.error.call_count, 1)
        self.assertEqual(mock_post.call_count, 0)
        blk.stop()

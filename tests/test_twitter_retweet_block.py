from unittest.mock import patch, MagicMock
from ..twitter_retweet_block import TwitterRetweet
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase


class TestTwitterRetweet(NIOBlockTestCase):

    @patch.object(TwitterRetweet, '_authorize')
    @patch.object(TwitterRetweet, '_retweet_tweet')
    def test_process_signal(self, mock_post, mock_auth):
        signals = [Signal({'id': 123})]
        blk = TwitterRetweet()
        self.configure_block(blk, {})
        blk.start()
        blk.process_signals(signals)
        mock_post.assert_called_once_with(signals[0].id)
        blk.stop()

    @patch.object(TwitterRetweet, '_authorize')
    @patch.object(TwitterRetweet, '_retweet_tweet')
    def test_process_multiple(self, mock_post, mock_auth):
        signals = [
            Signal({'id': 123}),
            Signal({'id': 456}),
            Signal({'id': 789})
        ]
        blk = TwitterRetweet()
        self.configure_block(blk, {})
        blk.start()
        blk.process_signals(signals)
        self.assertEqual(mock_post.call_count, len(signals))
        blk.stop()

    @patch.object(TwitterRetweet, '_authorize')
    @patch.object(TwitterRetweet, '_retweet_tweet')
    def test_bad_config(self, mock_post, mock_auth):
        signals = [Signal({'id': 123})]
        blk = TwitterRetweet()
        self.configure_block(blk, {'tweet_id': '{{id+2}}'})
        blk.logger.error = MagicMock()
        blk.start()
        blk.process_signals(signals)
        self.assertEqual(blk.logger.error.call_count, 1)
        self.assertEqual(mock_post.call_count, 0)
        blk.stop()

    @patch.object(TwitterRetweet, '_authorize')
    @patch.object(TwitterRetweet, '_retweet_tweet')
    def test_bad_id(self, mock_post, mock_auth):
        signals = [Signal({'id': 'asdf'})]
        blk = TwitterRetweet()
        self.configure_block(blk, {})
        blk.logger.error = MagicMock()
        blk.start()
        blk.process_signals(signals)
        self.assertEqual(blk.logger.error.call_count, 1)
        self.assertEqual(mock_post.call_count, 0)
        blk.stop()

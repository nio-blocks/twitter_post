import json
from unittest.mock import patch
from ..twitter_post_block import TwitterPost
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase


class TestTwitterPost(NIOBlockTestCase):
    @patch.object(TwitterPost, '_authorize')
    @patch.object(TwitterPost, '_post_tweet')
    def test_process_post(self, mock_post, mock_auth):
        signals = [Signal({'foo': 'test signal'})]
        blk = TwitterPost()
        self.configure_block(blk, {
            "status_update": "{{$foo}}"
        })
        blk.start()
        self.assertEqual(mock_auth.call_count, 1)

        blk.process_signals(signals)
        mock_post.assert_called_once_with({'status': signals[0].foo})
        blk.stop()

    @patch.object(TwitterPost, '_authorize')
    @patch.object(TwitterPost, '_post_tweet')
    def test_process_multiple(self, mock_post, mock_auth):
        signals = [
            Signal({'foo': 'test signal'}),
            Signal({'foo': 'another test'}),
            Signal({'foo': 'one more time'})
        ]
        blk = TwitterPost()
        self.configure_block(blk, {
            "status_update": "{{$foo}}"
        })
        blk.start()
        self.assertEqual(mock_auth.call_count, 1)
        blk.process_signals(signals)
        self.assertEqual(mock_post.call_count, len(signals))

        blk.stop()

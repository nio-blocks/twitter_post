# Twitter REST API Blocks
Blocks that interact with Twitter's [REST API](https://dev.twitter.com/rest/public).

This repository includes blocks that will [post] to a Twitter account, [favorite] posts, and [retweet] statuses.


Twitter Base Block
=======================
Base block that connects to the Twitter REST API using OAuth.

Properties
----------
* **consumer_key**: Twitter API key
* **app_secret**: Twitter API secret
* **oauth_token**: Twitter access token
* **oauth_token_secret**: Twitter access token secret

Dependencies
----------
* [requests_oauthlib](https://pypi.python.org/pypi/requests-oauthlib)

***

Twitter Post Block
=======================
A block that posts a tweet to a Twitter account.

Properties
----------
* **status**: content to post in tweet

Dependencies
----------
None

Input
----------
Any list of signals.

Output
----------
None. The `status` content is posted to Twitter.

***

Twitter Favorite Block
=======================
A block that favorites tweets on Twitter.

Properties
----------
* **id**: identifier for specified tweet to favorite

Dependencies
----------
None

Input
----------
Any list of signals.

Output
----------
None. The tweet with the correct `id` is favorited.

***

Twitter Retweet Block
=======================
A block that retweets posts on Twitter.

Properties
----------
* **id**: identifier for specified post to retweet

Dependencies
----------
None

Input
----------
Any list of signals.

Output
----------
None. The post with the correct `id` is retweeted.

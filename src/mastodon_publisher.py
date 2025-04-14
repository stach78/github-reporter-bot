from mastodon import Mastodon

class MastodonPublisher:
    def __init__(self, api_base_url, access_token):
        self.api_base_url = api_base_url
        self.access_token = access_token
        self.mastodon = Mastodon(access_token=self.access_token, api_base_url=self.api_base_url)

    def post_update(self, message):
        """Post a message to Mastodon"""
        self.mastodon.status_post(message)

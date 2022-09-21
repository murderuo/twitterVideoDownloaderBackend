import requests
import json
import re


class TwitterDownloadUrlGetter:

    extreme_bearer_token="Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"

    def __init__(self,id):
        self.id=id
        self.video_player_prefix = 'https://twitter.com/i/videos/tweet/'
        self.video_api_url = 'https://api.twitter.com/1.1/videos/tweet/config/'
        self.session=requests.Session()

    def __get_guest_token(self):
        guest_token_url="https://api.twitter.com/1.1/guest/activate.json"
        self.guest_token_response= self.session.post(guest_token_url)
        self.guest_token_response_json_data=json.loads(self.guest_token_response.text)
        # self.session.headers.update({'x-guest-token':self.guest_token_response_json_data.get('guest_token')})
        self.guest_token=self.guest_token_response_json_data.get('guest_token')
        return self.guest_token

    def __get_bearer_token(self):
        video_player_url=self.video_player_prefix+self.id
        video_player_url_response=self.session.get(video_player_url).text
        js_file_url = re.findall('src="(.*js)', video_player_url_response)[0]
        js_file_response=self.session.get(js_file_url).text
        bearer_token_pattern = re.compile('Bearer ([a-zA-Z0-9%-])+')
        bearer_token = bearer_token_pattern.search(js_file_response)
        bearer_token = bearer_token.group(0)
        return bearer_token

    def get_video_url(self):
        json_link = "https://api.twitter.com/1.1/statuses/show/" + self.id + ".json?&tweet_mode=extended"
        self.bearer_token=self.__get_bearer_token()
        self.session.headers.update({'Authorization':self.bearer_token})
        self.get_video_url_json=self.session.get(json_link).json()










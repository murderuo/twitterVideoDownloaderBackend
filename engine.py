import requests
import json
import re


class TwitterDownloadUrlGetter:



    def __init__(self,id):
        self.id=id
        self.video_player_prefix = 'https://twitter.com/i/videos/tweet/'
        self.video_api_url = 'https://api.twitter.com/1.1/videos/tweet/config/'
        self.session=requests.Session()
        self.extreme_bearer_token="Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
        # self.data={'video_file':'','latest_videos':[]}



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
        self.get_video_url_response=self.session.get(json_link)
        # print(self.get_video_url_response.text)
        will_be_check_json_data=self.get_video_url_response.json()
        control_result=self.check_data(will_be_check_json_data)
        if control_result==404: return 404
        if self.get_video_url_response.status_code==200:
            self.get_video_url_json=self.get_video_url_response.json()
            self.downloadable_url=self.url_extracter(self.get_video_url_json)
            self.save_a_txt_file(self.downloadable_url)
            return self.downloadable_url

    def check_data(self,json_data):
        if "extended_entities" not in json_data: return 404

        if 'media' not in json_data['extended_entities']:return 404

        if 'video_info' not in json_data["extended_entities"]["media"][0]:return 404




    def url_extracter(self,json_data):
        try:
            # url=resp["extended_entities"]["media"][0]["video_info"]["variants"][0]["url"] #this is one video file
            variants = json_data["extended_entities"]["media"][0]["video_info"]["variants"]
            bitrate = 0
            chosen_video = ""
            for i in range(len(variants)):
                if variants[i]['content_type'] == "application/x-mpegURL": continue
                # print(variants[i])
                if variants[i]['bitrate'] > bitrate:
                    bitrate = variants[i]['bitrate']
                    # self.data['video_file'] = variants[i]["url"]
                    chosen_video= variants[i]["url"]
            return chosen_video
        except:
            # print("video url not found..trying extreme method. ")

            new_header = {"Authorization": self.extreme_bearer_token}
            self.session.headers.update(new_header)
            json_link = "https://api.twitter.com/1.1/statuses/show/" + self.id + ".json?&tweet_mode=extended"
            resp2 = self.session.get(json_link).json()
            variants = resp2["extended_entities"]["media"][0]["video_info"]["variants"]
            # print(variants)
            bitrate = 0
            chosen_video = ""
            for i in range(len(variants)):
                if variants[i]['content_type'] == "application/x-mpegURL":
                    continue
                elif variants[i]['bitrate'] > bitrate:
                    bitrate = variants[i]['bitrate']
                    chosen_video = variants[i]["url"]
                    # self.data['video_file'] = variants[i]["url"]
            return chosen_video

    def save_a_txt_file(self,url):
        with open('url_db.txt',mode='a') as db:
            db.write(url)
            db.write('\n')
            db.close()

    def read_a_txt_file(self):
        with open('url_db.txt','r') as db:
            lines =db.readlines()
            # self.data['latest_videos']=lines[-4]
            return lines[-4:]

    def latest_videos(self):
        videos=self.read_a_txt_file()
        return videos





if __name__=='__main__':
    # id='1574298110981021697'
    id='1442369298366967808'
    downloadable_url = TwitterDownloadUrlGetter(id)
    url = downloadable_url.get_video_url()

    lines=downloadable_url.read_a_txt_file()
    # print(lines)
    print(url)
















import requests

import json
import configparser

config = configparser.RawConfigParser()
config.read('./twitter-token.properties')

base_url = config.get(section='AUTH', option='base.url')
bearer_token = config.get(section='AUTH', option='bearer.token')

tweet_fields = "tweet.fields=attachments,author_id,context_annotations,conversation_id,created_at,edit_controls," \
               "entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets," \
               "reply_settings,source,text,withheld"  # ,organic_metrics,promoted_metrics
user_fields = "user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url," \
              "protected,public_metrics,url,username,verified,verified_type,withheld"


def get_tweet_by_id_url(tweet_id_csv):
    ids = "ids=" + tweet_id_csv
    url = base_url + "/2/tweets?{}&{}".format(ids, tweet_fields)
    return url


def get_tweets_by_username_url(username):
    url = base_url + "/2/users/{}/tweets?{}".format(username, tweet_fields)
    return url


def get_user_by_username_url(username):
    url = base_url + "/2/users/by/username/{}?{}&{}".format(username, tweet_fields, user_fields)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    # url = get_user_by_username_url('')
    # url = get_tweet_by_id_url()
    url = get_tweets_by_username_url('1630479461622906880')
    json_response = connect_to_endpoint(url)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()

import os
import json
import time
import logging

import google_auth_oauthlib.flow
import google.oauth2.credentials
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from daemons.prefab import run
from draw_text import draw_thumbnail

scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]

VIDEO_ID = "4jfa0o7P-BA"

UPLOAD_TIME = 1609274610

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
WEEK = 7 * DAY
MONTH = 30 * DAY
YEAR = 365 * DAY


def credentials_to_dict(credentials) -> dict:
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }


class UpdateYoutubeVideoDeamon(run.RunDaemon):
    def run(self):
        """
        This function will update the thumbnail and title of the video linked to the ID given above.
        It measures the time difference since the upload, as well as counting the views and comments.

        After that, a thumbnail with these information is drawn, and the video is updated. This will run every 20
        Minutes, so that those information is kept up to date.
        """
        api_service_name = "youtube"
        api_version = "v3"

        # client_secrets_file = "client_secret.json"
        # Get credentials and create an API client
        # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        #     client_secrets_file, scopes)
        # credentials = credentials_to_dict(flow.run_console())

        with open(os.path.join(os.getcwd(), "credentials.json")) as infile:
            credentials = json.load(infile)

        while True:
            with open(os.path.join(os.getcwd(), "credentials.json"), 'w') as outfile:
                json.dump(credentials, outfile, indent=2)

            with open(os.path.join(os.getcwd(), "credentials.json")) as infile:
                credentials = json.load(infile)
            credentials = google.oauth2.credentials.Credentials(**credentials)
            youtube = googleapiclient.discovery.build(
                api_service_name, api_version, credentials=credentials)
            credentials = credentials_to_dict(credentials)

            current_time = time.time()
            time_delta = current_time - UPLOAD_TIME
            time_delta_str = ""
            if 0 <= time_delta < HOUR:
                time_delta = int(time_delta / MINUTE)
                time_delta_str = str(time_delta) + " minute"
            elif HOUR <= time_delta < DAY:
                time_delta = int(time_delta / HOUR)
                time_delta_str = str(time_delta) + " hour"
            elif DAY <= time_delta < WEEK:
                time_delta = int(time_delta / DAY)
                time_delta_str = str(time_delta) + " day"
            elif WEEK <= time_delta < MONTH:
                time_delta = int(time_delta / WEEK)
                time_delta_str = str(time_delta) + " week"
            elif MONTH <= time_delta < YEAR:
                time_delta = int(time_delta / MONTH)
                time_delta_str = str(time_delta) + " month"
            elif YEAR <= time_delta:
                time_delta = int(time_delta / YEAR)
                time_delta_str = str(time_delta) + " year"

            if time_delta > 1:
                time_delta_str += "s"

            request = youtube.videos().list(
                part="statistics",
                id=VIDEO_ID
            )
            response = request.execute()

            stats = response['items'][0]['statistics']
            view_count = stats['viewCount']
            like_count = stats['likeCount']
            comment_count = stats['commentCount']

            def format_counter(count: str) -> str:
                count = int(count)
                if 1000 <= count < 10000:
                    if int(count / 100) % 10 == 0:  # if count is between 1.000 and 1.099
                        return "1K"
                    return str(int(count / 100) / 10) + "K"   # if count is between 1.100 and 9.999 return "{n}.{d}K"
                elif 10000 <= count < 1000000:   # if count is between 10.000 and 999.999 return "{n}K"
                    return str(int(count / 1000)) + "K"
                elif 1000000 <= count < 10000000:
                    if int(count / 100000) % 10 == 0:  # if count is between 1.000.000 and 1.099.999
                        return "1M"
                    return str(int(count / 100000) / 10) + "M"  # if count is between 1.100.000 and 9.999.999 return "{n}.{d}M"
                elif 10000000 < count:
                    return str(int(count / 1000000)) + "M"  # if count is between 10.000.000 and 999.999.999 return "{n}M"
                return str(count)  # if count is under 1000 return count without rounding

            title = f"{time_delta_str} ago."
            subtitle = f"Has {format_counter(view_count)} views"
            other_subtitle = f"with {format_counter(like_count)} likes and {comment_count} comments"

            draw_thumbnail(title, subtitle, other_subtitle)
            request = youtube.thumbnails().set(
                videoId=VIDEO_ID,
                media_body=MediaFileUpload(os.path.join(os.getcwd(), "thumbnail.jpg"))
            )
            request.execute()
            request = youtube.videos().update(
                part="snippet",
                body={
                    "id": VIDEO_ID,
                    "snippet": {
                        "categoryId": 22,
                        "defaultLanguage": "en",
                        "title": f"This video was uploaded {time_delta_str} ago, has {format_counter(view_count)} views with {format_counter(like_count)} likes and {comment_count} comments.",
                        "description": """
DISCLAIMER!!: It can take up to 10 minutes for the thumbnail to update
reload the page and watch it update.
The github project for this video can be found on: https://github.com/SeJV/UpdatableYoutube



i will be updating this every hour or minute (sometimes)
comment and mark what time you commented at so you can
be really confused 2 years from now


This Video is not in Reverse.
This Video Has 26,564,302 Views
this video was uploaded 1 day ago.
this video was uploaded 6 days ago
this video has around 210k comments
why did you get this video to 100,000 likes
this video could get recommended
it's mathematically unlikely for mrbeast to comment on this video
MrBeast commented on my video
this video was uploaded 1 week ago
this video was uploaded 1 month ago
All comments in this video will be hearted
MrBeast will not comment in this video
Thank you MrBeast for commenting on my video
Don't click this video using your tongue
Comment is disabled until this video hit 10k likes
Thanos will not comment in this video
This video will not have verified comments
I magnet your finger to make you click this video
Comments will say their place
This video will not be age restricted
This video is not free pay to watch
This video will never get any verified comments
Don't turn on subtitle.
Comment is disabled until this video hit 10k likes
if MrBeast comments on this video, i will delete this video.
This video has only one comment
This video will be deleted in 5 days.
This video will not get recommended again.
This video will not reach 100K comments.
This video will not reach 100K views.
This video will not get recommended.
This video will be deleted in 7 days.
This video is not a speedrun.
This Video Has 26,564,302 Views
Press This Button To Win $100,000
Get This Random Person 1,000,000 Subscribers
This video has views
Dynamic updatable Title
Dynamic updatable Thumbnail"""
                    }
                }
            )
            response = request.execute()
            logging.info("UPDATED TO: ", response["snippet"]["title"])
            time.sleep(MINUTE)

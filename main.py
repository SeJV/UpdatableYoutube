# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import time

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

UPLOAD_TIME = 1609274732
MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
WEEK = 7 * DAY
MONTH = 30 * DAY
YEAR = 365 * DAY


def main():
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    while True:
        current_time = time.time()
        time_delta = current_time - UPLOAD_TIME
        sleep_for = MINUTE
        if 0 <= time_delta < HOUR:
            time_delta = str(round(time_delta / MINUTE)) + " minutes"
        elif HOUR <= time_delta < DAY:
            time_delta = str(round(time_delta / HOUR)) + " hours"
        elif DAY <= time_delta < WEEK:
            sleep_for = HOUR
            time_delta = str(round(time_delta / DAY)) + " days"
        elif WEEK <= time_delta < MONTH:
            sleep_for = DAY
            time_delta = str(round(time_delta / WEEK)) + " weeks"
        elif MONTH <= time_delta < YEAR:
            sleep_for = WEEK
            time_delta = str(round(time_delta / MONTH)) + " months"
        elif YEAR <= time_delta:
            sleep_for = MONTH
            time_delta = str(round(time_delta / YEAR)) + " years"

        request = youtube.videos().update(
            part="snippet",
            body={
                "id": "4jfa0o7P-BA",
                "snippet": {
                    "categoryId": 22,
                    "defaultLanguage": "en",
                    "title": f"This video was uploaded {time_delta} ago.",
                    "description": """
                        reload the page and watch it update.
                        the github project for this video can be found on: https://github.com/SeJV/UpdatableYoutube

                        i will be updating this every hour or minute (sometimes)
                        comment and mark what time you commented at so you can
                        be really confused 2 years from now
                        
                        
                        This Video is not in Reverse.
                        This Video Has 26,564,302 Views
                        this video was uploaded 1 day ago.
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
                        This video will not reach 1M views.
                        This video will not get recommended.
                        This video will be deleted in 7 days.
                        This video will be deleted in 1 month.
                        This video is not a speedrun.
                        This Video Has 26,564,302 Views
                        This video has views"""
                }
            }
        )
        response = request.execute()
        print('UPDATED TO: ', response['snippet']['title'])
        time.sleep(sleep_for)


if __name__ == "__main__":
    main()
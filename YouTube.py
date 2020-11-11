import os


import googleapiclient.discovery
import googleapiclient.errors

API_KEY = os.environ["YOUTUBE_KEY"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def search_videos(video_category, video_duration):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.

    # Get credentials and create an API client

    youtube = googleapiclient.discovery.build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY
    )

    request = youtube.search().list(
        part="snippet",
        maxResults=5,
        q=f"{video_category} -ASMR|asmr|Song|Game",
        type="video",
        safeSearch="strict",
        videoDuration=video_duration,  # short, medium, or long
        videoEmbeddable="true",
    )
    search_response = request.execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(
                (
                    search_result["snippet"]["title"],
                    search_result["id"]["videoId"],
                    # search_result["snippet"]["publishedAt"],
                    # search_result["snippet"]["description"],
                )
            )

    return videos


# def search_fan_videos(video_duration):
#     # Disable OAuthlib's HTTPS verification when running locally.
#     # *DO NOT* leave this option enabled in production.

#     # Get credentials and create an API client

#     youtube = googleapiclient.discovery.build(
#         YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY
#     )

#     request = youtube.search().list(
#         part="snippet",
#         maxResults=5,
#         q="fan sleep sounds -ASMR|asmr|Song|Thunder|",
#         type="video",
#         safeSearch="strict",
#         videoDuration=video_duration,  # short, medium, or long
#         videoEmbeddable="true",
#     )
#     search_response = request.execute()

#     videos = []

#     for search_result in search_response.get("items", []):
#         if search_result["id"]["kind"] == "youtube#video":
#             videos.append(
#                 (
#                     search_result["snippet"]["title"],
#                     search_result["id"]["videoId"],
#                     # search_result["snippet"]["publishedAt"],
#                     # search_result["snippet"]["description"],
#                 )
#             )

#     return videos


# if __name__ == "__main__":
#     search_short_rain_videos()

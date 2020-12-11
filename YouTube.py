import os


import googleapiclient.discovery
import googleapiclient.errors

API_KEY = os.environ["YOUTUBE_KEY"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def search_videos(video_category, video_duration):
    """Return filtered list filtered videos"""

    youtube = googleapiclient.discovery.build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY
    )

    request = youtube.search().list(
        part="snippet",
        maxResults=5,
        q=f"{video_category} -ASMR|asmr|Song|Game",
        type="video",
        safeSearch="strict",
        videoDuration=video_duration,
        videoEmbeddable="true",
    )
    search_response = request.execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(
                (search_result["snippet"]["title"], search_result["id"]["videoId"],)
            )

    return videos


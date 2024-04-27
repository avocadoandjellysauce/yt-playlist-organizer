from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re

def get_playlist_videos(api_key, playlist_id):
    '''takes in user API key and youtube playlist ID and returns pl_title and a dict {video titles: video descriptions}'''
    youtube = build('youtube', 'v3', developerKey=api_key)   #initialize API

    #getting playlist title
    playlist_response = youtube.playlists().list(
        part="snippet",
        id=playlist_id
    ).execute()
    pl_title = playlist_response['items'][0]['snippet']['title']
    #print(f"Playlist Title: {playlist_title}\n")

    # Get the videos in the playlist
    videos_response = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=15 # 50 videos is the Maximum allowed by YouTube Data API
    ).execute()

    pl_data = {}
    # parsing for video titles and their descriptions from videos_response API return 
    for video in videos_response['items']:
        video_title = video['snippet']['title']
        video_description = video['snippet']['description'].replace('\n', '')

        # It is common for youtube descriptions to contain promotional content, shoutouts, sponsorships, outside links
        # To optimize relevance of the description, extract description info until first instance of certain keywords
        # namely: http (for outside links), shoutout, shout out, check out.
        # This pattern looks for text before the first occurrence of the specified keywords
        pattern = r"^(.*?)(?=http|shoutout|shout out|check out|sign up|newsletter|sponsor)"
        match = re.search(pattern, video_description, re.IGNORECASE | re.DOTALL)
        if match:
            # Extract the relevant description
            video_description = match.group(1).strip()

        # add filtered video_description to pl_data dict
        pl_data[video_title] = video_description
        #print(f"Video Title: {video_title}\nDescription: {video_description}\n")
    return pl_title, pl_data


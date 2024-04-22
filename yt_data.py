from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
        video_description = video['snippet']['description']
        pl_data[video_title] = video_description
        #print(f"Video Title: {video_title}\nDescription: {video_description}\n")
    return pl_title, pl_data


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import OAuth2WebServerFlow
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from yt_data import *

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('punkt')
lemmatizer = WordNetLemmatizer()
import string


# test code for api call using api key !
# api_key = "AIzaSyDC3oxqRypaOGAA6AgzeOoYaNzYhhxV00c" # API key for Youtube Data API
# youtube = build('youtube', 'v3', developerKey=api_key)   #initialize API

def main():
    # Initializing oAuth2
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json", scopes = ['https://www.googleapis.com/auth/youtube']
    )
    # Runs consent screen for the app to manage YouTube account
    flow.run_local_server(port=8080, prompt='consent')
    # Credentials needed to call YouTube Data Api
    credentials = flow.credentials

    # youtube object will be used to make calls to YouTube Data Api
    youtube = build('youtube', 'v3', credentials=credentials)
   
    # get playlist ID
    # playlist id is the string after 'list=' in a URL: https://www.youtube.com/playlist?list=PLJzPmoq-bebri51Ih1E8cOT_23JmQtSBl
    playlist_id = "PLJzPmoq-bebri51Ih1E8cOT_23JmQtSBl"  # this ID is a demo playlist from TED-ED

    # extracting info from selected playlist. See yt_data.py
    try:
        pl_title, pl_data, url_dict, youtube = get_playlist_videos(youtube, playlist_id)
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")


    # ask user for amount of subplaylists, their titles, and keywords relevant to content
    n_subplaylists = int(input('How many subplaylists would you like to create? > '))
    subplaylist_info = {} # will contain {subplaylist title: [subplaylist keywords]}
    for i in range(n_subplaylists):
        subplaylist_title = input(f'Subplaylist #{i+1} title: ')
        keywords = input('Enter relevant keywords to your subplaylist content (comma seperated): ').lower().split(',')
        keywords.append(subplaylist_title)
        subplaylist_info[subplaylist_title] = keywords

    # playlist assignment
    playlist_assignments = assign_subplaylist(pl_data, subplaylist_info)
    #print(playlist_assignments)

    #Create subplaylists:
    subplaylist_ids = create_subplaylists(youtube, subplaylist_info)

    # add videos to subplaylists:
    add_videos_to_subplaylists(youtube, playlist_assignments, url_dict, subplaylist_ids)

        # list of the subplaylist names
    subplaylists = [pl for pl in subplaylist_info]
     
    # printing results for assigned playlists
    for sub in subplaylists:
        vids = []
        for video in playlist_assignments:
            if playlist_assignments[video] == sub:
                print(f'{video} was added to {sub} playlist. ')
        print()
    print()

    print('The following videos were not added to any playlist: ')
    for video in playlist_assignments:
        if playlist_assignments[video] == None:
            print(video)


if __name__ == "__main__":
    main()


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from yt_data import get_playlist_videos
from nlp import language_processing

def main():

    api_key = "AIzaSyDC3oxqRypaOGAA6AgzeOoYaNzYhhxV00c" # API key for Youtube Data API

    # playlist id is the string after list= in a URL: https://www.youtube.com/playlist?list=PLJzPmoq-bebri51Ih1E8cOT_23JmQtSBl
    playlist_id = "PLJzPmoq-bebri51Ih1E8cOT_23JmQtSBl"  #demo playlist TED-ED

    try:
        pl_title, pl_data = get_playlist_videos(api_key, playlist_id)
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")


    processed_pl_data = language_processing(pl_data)



if __name__ == "__main__":
    main()
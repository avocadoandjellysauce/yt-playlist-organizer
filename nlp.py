from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from yt_data import get_playlist_videos

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')

def language_processing(pl_data):
    '''processes keywords from pl_data dictionary'''
    # to begin processing the pl_data, we will need to tokenize (seperating title/description into words)
    # then we will remove the common stopwords, words that will not help in filtering the videos.

    filtered_pl_data = {}
    stopwords = set(stopwords.words('english'))  # set of common english stopwords from nltk
    for video_title in pl_data:
        token_title = word_tokenize(video_title)
        token_description = word_tokenize(pl_data[video_title])

        filtered_title = [word for word in token_title if word.casefold() not in stopwords]
        filtered_description = [word for word in token_description if word.casefold() not in stopwords]
        filtered_pl_data[filtered_title] = filtered_description
    
    return filtered_pl_data
    



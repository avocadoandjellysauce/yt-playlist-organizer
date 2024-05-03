import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from urllib.parse import urlparse, parse_qs

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
lemmatizer = WordNetLemmatizer()
import string

def extract_playlist_id(url):
    '''extracts playlist URL from input_playlist. If invalid, will return demo playlist from TED-ED: https://www.youtube.com/watch?v=y5XEwTDlriE&list=PLJzPmoq-bebri51Ih1E8cOT_23JmQtSBl'''
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    playlist_id = query_params.get('list', [''])[0]  # Default to empty string if not found
    
    if not playlist_id:
        playlist_id = "PLJzPmoq-bebri51Ih1E8cOT_23JmQtSBl"  # this ID is a demo playlist from TED-ED
    
    return playlist_id

def get_playlist_videos(youtube, playlist_id):
    '''takes in youtube build and youtube playlist ID and returns pl_title, pl_data {video titles: video descriptions}, url_dict {video title: url}, and   updated youtube build object.
    video titles and descriptions will be tokenized and filtered down into their keywords'''
    
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
    url_dict = {}
    # parsing for video titles and their descriptions from videos_response API return 
    for video in videos_response['items']:
        video_title = video['snippet']['title']
        video_description = video['snippet']['description'].replace('\n', '')
        video_id = video['snippet']['resourceId']['videoId'] # Extract the video ID
        url_dict[video_title] = video_id

        # It is common for youtube descriptions to contain promotional content, shoutouts, sponsorships, outside links
        # To optimize relevance of the description, extract description info 
        # check for and filter out certain keywords namely: http (for outside links), shoutout, shout out, check out.
        
        # I will break the description into sentences, then filter out the less relevant sentences
        sentences = sent_tokenize(video_description)

        # This pattern looks for text before the first occurrence of the specified keywords
        pattern = r"^(.*?)(?=http|shoutout|shout out|check out|sign up|newsletter|sponsor)"

        # Removes all sentences if keywords in pattern are contained
        filtered_sentences = [sentence for sentence in sentences if not re.search(pattern, sentence, re.IGNORECASE)]
        video_description = ' '.join(filtered_sentences).strip()

        # now remove all non essential words with NLTK: stop words, Proper names (since often Patreon supporters are listed in descriptions), Note: proper names in video_titles are not removed
        stop_words = set(stopwords.words('english')) 

        # split into words

        token_description = word_tokenize(video_description)

        # removing stop words and punctuation
        filtered_description = [word for word in token_description if word.casefold() not in stop_words and word not in string.punctuation]

        # lemmatize the words,  essentially returning the base/dictionary form of a word aka the 'lemma' (source NLTK). This is done to improve match rates later on
        lemmatized_description = [lemmatizer.lemmatize(word) for word in filtered_description]

        # pos_tag returns list of tuples (word, part of speech), and removes all Singular Proper nouns (NNP) and plural Proper nouns (NNPS)
        tagged_description = pos_tag(lemmatized_description)
        filtered_description = [word for word, tag in tagged_description if tag not in ['NNP', 'NNPS']]

        # add filtered video_description to pl_data dict
        pl_data[video_title] = filtered_description


    return pl_title, pl_data, url_dict, youtube

def assign_subplaylist(pl_data, subplaylist_info):
    '''returns subplaylist assignment for each video in pl_data given subplaylist_info'''
    subplaylist_assignments = {}

    # for each video in pl_data:
    for video_title, video_description in pl_data.items(): 
        # video_title is string, video_description is a list of strings
        
        #initialize match_score dict to keep track of how closely the video matches each subplayist
        match_score = dict.fromkeys(subplaylist_info.keys(), 0)

        # Iterate through each subplaylist
        for subplaylist_title, keywords in subplaylist_info.items():
            # iterate through the given keywords of each subplaylist
            for keyword in keywords:
                if keyword in video_title.lower(): # if a keyword matches directly in video title, award 10 points
                    match_score[subplaylist_title] += 10
                if keyword in ' '.join([word.lower() for word in video_description]): # award 3 points if match in video description 
                    match_score[subplaylist_title] += 3
            if match_score[subplaylist_title] >= 20: # if more than 20 points, break and match video to playlist
                break
        
        # find highest match score 
        highest_score = max(match_score.values())
        if highest_score > 0:
            for subplaylist_title, score in match_score.items():
                if score == highest_score:
                    subplaylist_assignments[video_title] = subplaylist_title # assign to subplaylist
                    break

        else: # assign None if all match scores are 0
            subplaylist_assignments[video_title] = None
    
    return subplaylist_assignments
            
def create_subplaylists(youtube, subplaylist_info):
    """
    Creates subplaylists based on the provided subplaylist_info.
    Returns a dictionary mapping subplaylist titles to their IDs.
    """
    subplaylist_ids = {}
    for title, keywords in subplaylist_info.items():
        keywords_str = ', '.join(keywords)
        # Create a new playlist
        playlist_response = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": f"Subplaylist created by script with keywords used: [{keywords_str}]",
                    "tags": keywords
                },
                "status": {
                    "privacyStatus": "unlisted" # or "public" or "private"
                }
            }
        ).execute()
        subplaylist_ids[title] = playlist_response['id']
    return subplaylist_ids

def add_videos_to_subplaylists(youtube, subplaylist_assignments, url_dict, subplaylist_ids):
    """
    Adds videos to the corresponding subplaylists based on the assignments.
    """
    for video_title, subplaylist_title in subplaylist_assignments.items():
        if subplaylist_title is not None:
            video_id = url_dict[video_title]
            subplaylist_id = subplaylist_ids[subplaylist_title]
            # Add the video to the subplaylist
            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": subplaylist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            ).execute()

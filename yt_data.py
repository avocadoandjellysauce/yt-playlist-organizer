from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
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

def get_playlist_videos(api_key, playlist_id):
    '''takes in user API key and youtube playlist ID and returns pl_title and a dict {video titles: video descriptions}.
        video titles and descriptions will be tokenized and filtered down into their keywords'''
    
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

        #token_title = word_tokenize(video_title)

        token_description = word_tokenize(video_description)

        # removing stop words and punctuation
        #filtered_title = ' '.join([word for word in token_title if word.casefold() not in stop_words and word not in string.punctuation]) # turning into string since dict key can't be mutable type

        filtered_description = [word for word in token_description if word.casefold() not in stop_words and word not in string.punctuation]

        # lemmatize the words,  essentially returning the base/dictionary form of a word aka the 'lemma' (source NLTK). This is done to improve match rates later on
        lemmatized_description = [lemmatizer.lemmatize(word) for word in filtered_description]

        # pos_tag returns list of tuples (word, part of speech), and removes all Singular Proper nouns (NNP) and plural Proper nouns (NNPS)
        tagged_description = pos_tag(lemmatized_description)
        filtered_description = [word for word, tag in tagged_description if tag not in ['NNP', 'NNPS']]

        # add filtered video_description to pl_data dict
        pl_data[video_title] = filtered_description

        #print(f"Video Title: {video_title}\nDescription: {video_description}\n")

    return pl_title, pl_data, url_dict, youtube

def create_subplaylists(youtube, subplaylist_info):
    """
    Creates subplaylists based on the provided subplaylist_info.
    Returns a dictionary mapping subplaylist titles to their IDs.
    """
    subplaylist_ids = {}
    for title, keywords in subplaylist_info.items():
        # Create a new playlist
        playlist_response = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": "Subplaylist created by script",
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

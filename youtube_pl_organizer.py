from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import OAuth2WebServerFlow
from yt_data import *
import tkinter as tk
from tkinter import messagebox
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

def main():

    api_key = "AIzaSyDC3oxqRypaOGAA6AgzeOoYaNzYhhxV00c" # API key for Youtube Data API

    # playlist id is the string after list= in a URL: https://www.youtube.com/playlist?list=PLJzPmoq-bebri51Ih1E8cOT_23JmQtSBl
    playlist_id = "PLJzPmoq-bebri51Ih1E8cOT_23JmQtSBl"  #demo playlist from TED-ED

    try:
        pl_title, pl_data, url_dict, youtube = get_playlist_videos(api_key, playlist_id)
        #print(f'got playlist id: {playlist_id}')
        #print(pl_title, pl_data)
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")

    #print(pl_data)
    #processed_pl_data = language_processing(pl_data)
    #print(processed_pl_data)

    # retrieve user input for amount of subplaylists, their titles, and keywords relevant to content
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
    #subplaylist_ids = create_subplaylists(youtube, subplaylist_info)

    # add videos to subplaylists:
    #add_videos_to_subplaylists(youtube, playlist_assignments, url_dict, subplaylist_ids)

def assign_subplaylist(pl_data, subplaylist_info):
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
            



def submit_url(url_entry):
    url = url_entry.get()
    i = url.find('list=')
    if i:
        messagebox.showinfo("Checking URL")
        return url[i+5:]
    else:
        messagebox.showerror("Error", "Invalid URL or playlist ID not found.")
        

'''
    #initializing tkinter GUI
    root = tk.Tk()
    root.title("YouTube Playlist Organizer")

    tk.Label(root, text="Enter Playlist URL:").pack()
    url_entry = tk.Entry(root)
    url_entry.pack()

    submit_button = tk.Button(root, text="Submit", command=lambda: submit_url(url_entry))
    submit_button.pack()

    root.mainloop()
    '''
    
if __name__ == "__main__":
    main()


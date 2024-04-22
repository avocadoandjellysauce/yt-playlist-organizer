from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from yt_data import get_playlist_videos
from nlp import language_processing
import tkinter as tk
from tkinter import messagebox



def main():

    api_key = "AIzaSyDC3oxqRypaOGAA6AgzeOoYaNzYhhxV00c" # API key for Youtube Data API

    #initializing tkinter GUI
    root = tk.Tk()
    root.title("YouTube Playlist Organizer")

    tk.Label(root, text="Enter Playlist URL:").pack()
    url_entry = tk.Entry(root)
    url_entry.pack()

    submit_button = tk.Button(root, text="Submit", command=lambda: submit_url(url_entry))
    submit_button.pack()

    

    root.mainloop()

    # playlist id is the string after list= in a URL: https://www.youtube.com/playlist?list=PLJzPmoq-bebri51Ih1E8cOT_23JmQtSBl
    #playlist_id = "PLJzPmoq-bebri51Ih1E8cOT_23JmQtSBl"  demo playlist TED-ED

    try:
        #pl_title, pl_data = get_playlist_videos(api_key, playlist_id)
        print(f'got playlist id: {playlist_id}')
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")


    processed_pl_data = language_processing(pl_data)


def submit_url(url_entry):
    url = url_entry.get()
    i = url.find('list=')
    if i:
        messagebox.showinfo("Checking URL")
        return url[i+5:]
    else:
        messagebox.showerror("Error", "Invalid URL or playlist ID not found.")
        
    
if __name__ == "__main__":
    main()


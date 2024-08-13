# SPOTIFY API
import spotipy
import spotipy.util as util

# PRINTING JSON
from pprint import pprint

# ENV
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 


class Spotify:
    def __init__(self, printing = True):
        self.token = util.prompt_for_user_token(
            username=os.environ.get("SPOTIPY_USERNAME"),
            scope=self.get_scope(),
            show_dialog=True
        )
        
        if (printing):
            print(os.environ.get("SPOTIPY_REDIRECT_URI"))
            print(os.environ.get("SPOTIPY_CLIENT_ID"))
            print(os.environ.get("SPOTIPY_CLIENT_SECRET"))
            print(os.environ.get("SPOTIPY_USERNAME"))
            print(self.token)
            
        self.sp = spotipy.Spotify(auth=self.token)
        
        
        
    def get_scope(self):
        scope = [
            "user-read-private", 
            "user-read-email",
            "playlist-read-collaborative",
            "playlist-read-private",
            "streaming",
            "user-read-playback-state",
            "user-modify-playback-state",
            "user-read-currently-playing"
        ]
        return scope
    
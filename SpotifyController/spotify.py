# SPOTIFY API
import spotipy
import spotipy.util as util

# PRINTING JSON
from pprint import pprint

# DEVICE CLASS
from device import Device

# ENV
import os
from dotenv import load_dotenv
load_dotenv()


class Spotify:
    def __init__(self, printing=False):
        self.token = util.prompt_for_user_token(
            username=os.environ.get("SPOTIPY_USERNAME"),
            scope=self.get_spotify_scope(),
            show_dialog=False
        )

        if (printing):
            print(os.environ.get("SPOTIPY_REDIRECT_URI"))
            print(os.environ.get("SPOTIPY_CLIENT_ID"))
            print(os.environ.get("SPOTIPY_CLIENT_SECRET"))
            print(os.environ.get("SPOTIPY_USERNAME"))
            print(self.token)
            pprint(self.token)

        self.sp = spotipy.Spotify(auth=self.token)
        self.device = self.get_device()

    def get_spotify_scope(self):
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

    def get_device_list(self):
        devices_list = self.sp.devices()['devices']
        if devices_list == []:
            raise Exception("[ERROR] No devices were detected. Please ensure \
your Spotify Desktop App is open and try again.")
        return devices_list

    def get_device(self):
        try:
            devices_list = self.get_device_list()
        except Exception as error:
            print(error)
            exit()
        first_device_found = devices_list[0]
        device = Device(
            device_id=first_device_found['id'],
            device_is_active=first_device_found['is_active'],
            device_name=first_device_found['name'],
            device_supports_volume=first_device_found['supports_volume'],
            device_type=first_device_found['type'],
            device_volume_percent=first_device_found['volume_percent']
        )
        return device

    def compare_IDs(self, id_1, id_2):
        if id_1 != id_2:
            raise Exception("[ERROR] Different device connected.")
            print("Original ID:", id_1)
            print("New ID:", id_2)

    def device_active_check(self):
        is_active = self.device.device_is_active
        if not is_active:
            raise Exception("[ERROR] Device is not active.")

    def safety_check(self):
        try:
            recent_device = self.get_device()
        except Exception as error:
            print(error)
            exit()
        try:
            self.compare_IDs(self.device.device_id, recent_device.device_id)
        except Exception as error:
            print(error)
            exit()
        try:
            self.device_active_check()
        except Exception as error:
            print(error)
            exit()
        self.device = recent_device

    ''' GETTERS
    - Current Track provides a short list of valuable info about the current
    song.
    - Current Features provides a list of features of the song, such as energy,
    key, tempo, time signature, and so on.
    - Current Analysis provides too much info, not sure what to do with it.
    - Current Volume returns the current volume of the player.
    - Current Playback returns a boolean of the playback state.
    '''

    def get_current_track(self):
        if self.get_playback() is False:
            return None

        currently_playing = self.sp.currently_playing()
        track_id = currently_playing['item']['id']
        track_name = currently_playing['item']['name']
        artists = currently_playing['item']['artists']
        artists_name = ', '.join([artist['name'] for artist in artists])
        album_name = currently_playing['item']['album']['name']
        link = currently_playing['item']['external_urls']['spotify']
        uri = currently_playing['item']['uri']
        current_track_info = {
            "id": track_id,
            "name": track_name,
            "artists": artists_name,
            "album": album_name,
            "link": link,
            "uri": uri,
        }
        return current_track_info

    def get_song_features(self, song_uri=None):
        self.safety_check()
        if song_uri is None:
            song_uri = self.get_current_track()["uri"]
        features = self.sp.audio_features(song_uri)[0]
        return features

    def get_song_analysis(self, track_id=None):
        self.safety_check()
        if track_id is None:
            track_id = self.get_current_track()["id"]
        analysis = self.sp.audio_analysis(track_id)
        return analysis

    def get_playback(self):
        self.safety_check()
        playback = self.sp.current_playback()['is_playing']
        return playback

    def get_current_volume(self):
        self.safety_check()
        current_volume = self.device.device_volume_percent
        return current_volume

    ''' PLAYBACK FEATURES '''

    def play_current_track(self):
        self.safety_check()
        if not self.get_playback():
            self.sp.start_playback()

    def pause_current_track(self):
        self.safety_check()
        if self.get_playback():
            self.sp.pause_playback()

    def alternate_playback(self):
        if self.get_playback():
            self.pause_current_track()
        else:
            self.play_current_track()

    def play_next_track(self):
        self.safety_check()
        self.sp.next_track()

    def play_specific(self, track_uri):
        self.safety_check()
        try:
            self.sp.start_playback(context_uri=track_uri)
        except Exception as error:
            print("[ERROR] Invalid track_uri provided to play_specific.")
            print(error)
            exit()

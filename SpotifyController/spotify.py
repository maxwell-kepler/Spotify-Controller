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

        print(self.get_current_volume())
        pprint(self.get_playback())
        self.play_current_track()
        pprint(self.get_current_track())
        pprint(self.get_song_features())

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

import json
import math
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

#WebAPI creds
client_id = input('Enter client_id: ')
client_secret = input('Enter client_secret: ')
redirect_uri = input('Enter redirect URL (same as in your dashboard): ')

class Track:
    """Track object class for easier access to relevant properties"""
    def __init__(self, uri, name, added_at):
        self.uri = uri
        self.name = name
        self.added_at = added_at

def authorize_user_using_scopes():
    """Ask user to log in and authorize scopes via spotipy
    Returns spotipy Spotify object"""

    scope = 'playlist-read-private playlist-read-private playlist-modify-private playlist-modify-public'

    spotify = spotipy.Spotify(auth_manager = SpotifyOAuth(scope=scope, client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri, open_browser = True))
   
    return spotify

def spotipy_create_track_list(playlist_id, spotify):
    track_list = list()
    api_request_index = 0
    
    while bool(spotify.playlist_items(playlist_id, offset = api_request_index * 100)['items']):
        playlist_content = spotify.playlist_items(playlist_id, offset = api_request_index * 100)

        for track in playlist_content['items']:
            track_list.append(Track(track['track']['uri'], track['track']['name'], track['added_at']))

        api_request_index += 1

    return track_list

def convert_track_list_to_dictionary(track_list):
    """Converts a list of Track objects into a dictionary"""
    track_dict = dict()
    for element in track_list:
        if element.uri not in track_dict:
            track_dict[element.uri] = {'name': element.name, 'added_at': element.added_at}
    return track_dict

def get_user_playlist_id(prompt):
    """Gets playlist url from user and returns the playlist id"""
    playlist_id = str()
    
    while playlist_id == '':
        user_input = input(prompt)
        if 'https://open.spotify.com/playlist/' in user_input:
            user_input.replace('https://open.spotify.com/playlist/', '')

            playlist_id_end_index = user_input.find('?')
            if playlist_id_end_index != -1:
                user_input[:playlist_id_end_index]
            
            playlist_id = user_input
        else:
            print('Invalid url.')
    
    return playlist_id

#Main program -----------------------------------------------------------------------------------------------------------------

#Authorization using client credentials
spotify = authorize_user_using_scopes()

#Get two playlists and append them into one
track_list_1 = spotipy_create_track_list(get_user_playlist_id('Enter playlist URL of the first playlist: '), spotify)
track_list_2 = spotipy_create_track_list(get_user_playlist_id('Enter playlist URL of the second playlist: '), spotify)

merged_track_list = track_list_1 + track_list_2

#Sort the playlist based on date added
def get_date(track):
    return track.added_at

merged_track_list.sort(key=get_date)

#Convert playlist into dictionary (removes duplicates) and dump it into a json for checking
merged_track_dict = convert_track_list_to_dictionary(merged_track_list)

with open("merged_playlist.json", "w") as outfile:
    json.dump(merged_track_dict, outfile, indent=4)

#Print out the playlist dictionary for checking
for track in merged_track_dict:
    print(merged_track_dict[track]['name'] + ': ' + merged_track_dict[track]['added_at'])

#Ask user for confirmation before posting api request
if input('Proceed to uploading? y/n: ') == 'n':
    exit()

#Add tracks to provided playlist based on uris from the playlist dictionary by 100 track chunks
merged_playlist_id = get_user_playlist_id('Enter URL of playlist to add tracks to: ')

post_request_index = 0
while post_request_index < math.ceil(len(merged_track_dict) / 100):
    print('Adding tracks ' + str(post_request_index * 100) + ' - ' + str(post_request_index * 100 + 99))
    spotify.playlist_add_items(merged_playlist_id, list(merged_track_dict.keys())[post_request_index * 100 : post_request_index * 100 + 100])

    post_request_index += 1

print('Added tracks to playlist.')

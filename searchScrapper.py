#! /usr/bin/env python3
import spotipy
from spotipy import util
from spotipy.oauth2 import SpotifyClientCredentials
import time, random
# Spotify API client id and client secret imports
from config import *


def get_all_uris(arr):
    """ Get all uris in arr.

    Args:
        arr: Dictionary where uris are contained.

    Return:
        uris: An array containing all uris retrieved.
    """
    uris = []

    for i in range(len(arr['items'])):
        uris.append(arr['items'][i]['uri'])

    return uris


def retrieve_all_songs_and_ids(sp, uris, spotify_songs, spotify_songs_ids):
    """ Retrieve all songs and their ids using spotipy.

    Args:
        sp: Spotify object to access API.
        uris: An array containing all uris.
        spotify_songs: A set containing all the song names.
        spotify_songs_ids: An array containing all the corresponding song ids.
    """
    for i in range(len(uris)):
        tracks = sp.album_tracks(uris[i])

        for n in range(len(tracks['items'])):
            if tracks['items'][n]['name'] not in spotify_songs:
                spotify_songs.add(tracks['items'][n]['name'])
                spotify_songs_ids.append(tracks['items'][n].get('id'))


def retrieve_all_songs_and_ids_app(sp, name, uris, spotify_songs, spotify_songs_ids):
    """ Retrieve all songs and their ids on appears_on using spotipy.

    Args:
        sp: Spotify object to access API.
        name: Name of artist.
        uris: An array containing all uris.
        spotify_songs: A set containing all the song names.
        spotify_songs_ids: An array containing all the corresponding song ids.
    """
    for i in range(len(uris)):
        tracks = sp.album_tracks(uris[i])

        for n in range(len(tracks['items'])):
            for g in tracks['items'][n]['artists']:
                if g.get('name') == name:
                    if tracks['items'][n]['name'] not in spotify_songs:
                        spotify_songs.add(tracks['items'][n]['name'])
                        spotify_songs_ids.append(tracks['items'][n].get('id'))


def add_songs_to_playlist(username, playlist_id, client_id, client_secret, spotify_songs_ids):
    """ Add all songs with ids in spotify_songs_ids into a Spotify playlist.

    Args:
        username: Spotify username.
        playlist_id: Spotify playlist id.
        client_id: Spotify client id.
        client_secret: Spotify client secret.
        spotify_songs_ids: An array containing all song ids.
    """
    # Get authentication
    token = util.prompt_for_user_token(username,
                                       scope='playlist-modify-private,playlist-modify-public',
                                       client_id=client_id,
                                       client_secret=client_secret,
                                       redirect_uri='http://localhost:8888/callback/')

    # If authentication is given add songs to playlist
    if token:
        song_count = len(spotify_songs_ids)
        bindex = 0
        endindex = bindex + 98
        sp = spotipy.Spotify(auth=token)

        while (True):
            if song_count - 98 <= 0:
                sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id,
                                            tracks=spotify_songs_ids)
                break
            elif endindex >= song_count:
                sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id,
                                            tracks=spotify_songs_ids[bindex:song_count])
                break
            else:
                sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id,
                                            tracks=spotify_songs_ids[bindex:endindex])
                bindex = endindex + 1
                endindex = bindex + 98

            # Random time scrapping
            time.sleep(random.randint(10, 20))

        print('done')
    else:
        print('Unable to get token')


def main():
    """ Interface to receive user input.
    """
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    # Spotify object to access API
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Get artist to search
    name = input("Artist name: ")
    results = sp.search(q='artist:' + name, type='artist')

    # Get artist uri
    for i in results['artists']['items']:
        if i['uri'] is not None:
            artist_uri = i['uri']
            break

    # Get all of artist's songs
    sp_singles = sp.artist_albums(artist_uri, album_type='single')
    sp_albums = sp.artist_albums(artist_uri, album_type='album')
    sp_appears_on = sp.artist_albums(artist_uri, album_type='appears_on')

    # Store uris
    album_uris = get_all_uris(sp_albums)
    single_uris = get_all_uris(sp_singles)
    appears_on_uris = get_all_uris(sp_appears_on)

    # Retrieve all song names and ids
    spotify_songs_names = set()
    spotify_songs_ids = []
    retrieve_all_songs_and_ids(sp, album_uris, spotify_songs_names, spotify_songs_ids)
    retrieve_all_songs_and_ids(sp, single_uris, spotify_songs_names, spotify_songs_ids)
    retrieve_all_songs_and_ids_app(sp, name, appears_on_uris, spotify_songs_names, spotify_songs_ids)

    # Print all artist's songs and the number of songs on Spotify
    print(spotify_songs_names)
    print("Number of Songs: " + str(len(spotify_songs_ids)))

    # Ask if they want to put all the songs in one of their playlists - y for yes put all songs in playlist
    download_playlist = input("Put y for Yes ... Enter for no"
                              + "\nWould you like to put all songs into one of your playlist on Spotify: ")

    if download_playlist == 'y':
        username = input("Enter Spotify username: ")
        playlist_id = input("Enter Playlist ID: ")
        add_songs_to_playlist(username, playlist_id, CLIENT_ID, CLIENT_SECRET, spotify_songs_ids)


main()





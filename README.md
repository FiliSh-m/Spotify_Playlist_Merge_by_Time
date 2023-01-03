# Spotify Playlist Merge by Time
Simple script to merge tracks from two playlists into a third based on addition time through Spotify WebAPI

**I do not plan to maintain this project. If something breaks, feel free to fix it.**

## Installation

Download the whole repo and extract it anywhere

Requires python to run the script.

Uses [spotipy](https://github.com/spotipy-dev/spotipy) python library to access the Spotify WebAPI, install it using this command:

```
pip install spotipy
```

## Usage
1. **Get Spotify WebAPI credentials**
    
    Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and create a new App. Provide any *redirect URL* and save it for later. Copy *client id* and *client secret* save them for later.

2. **Run the script**
    
    Navigate through command line to the folder the script is in and run it with python:    
    ```
    python3 Spotify_playlist_merge_by_time.py
    ```

3. **Follow instructions to enter required inputs**
    
    Provide WebAPI credentials from the developer dashboard when asked.
    
    Enter URLs of playlists to take tracks from (get it on Spotify through Share option)

4. **Add tracks to merged playlist**

    Script writes out all tracks to be added in correct order and also dumps them into a json file ```merged_playlist.json```.

    Approve that everything is correct when asked and provide URL of playlist to add tracks to (create it first yourself on Spotify if needed).

5. **Done**

    Tracks should be added into provided playlist in 100 track chunks due to API limitation and you should see a success message at the end.

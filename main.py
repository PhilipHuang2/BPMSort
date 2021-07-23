import spotipy
import json
import pprint
import numpy as np
import matplotlib.pyplot as plt
from spotipy.oauth2 import SpotifyOAuth

scope = "playlist-modify-public,playlist-modify-private,user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

print("Hey, we are loading your music to check it out.")
results = sp.current_user_saved_tracks()
playList = results['items']
while results['next']:
    results = sp.next(results)
    playList.extend(results['items'])

# taking in speed data
print("Now categorizing your music.")
total = len(playList)
speed = {}
playTime = {}
for idx, item in enumerate(playList):
    track = item['track']
    bpm = sp.audio_features(track['uri'])[0]['tempo']
    # int(bpm) for the bpm of each track round to the digits place
    # int(round(bpm, -1)) for the bpm of each track rounded to the tenth place
    roundedBPM = int(round(bpm, -1))
    speed.setdefault(roundedBPM, []).append(track['uri'])
    playTime.setdefault(roundedBPM, 0)
    playTime[roundedBPM] += track['duration_ms']
    print(idx, "out of", total, "songs checked.")
    # print(idx, track['artists'][0]['name'], " – ", track['name'], "- BPM:", int(bpm))

# print out results.
print("Hey, we have finished categorizing your music.  Here is what we have found.")
options = []
for key, value in sorted(speed.items()):
    options.append(key)
    print("You have", len(value), "songs that are", key,  "BPM for a total playtime of", str(int(playTime[key]/60000)) + ":" + str(int(playTime[key]/1000 % 60)), "minutes.")
goodInput = False
while not goodInput:
    bpmInput = input("Please choose a BPM to create a playlist for: ")
    bpmInput = int(bpmInput)
    if bpmInput in speed.keys():
        goodInput = True
    else:
        input("That is not a valid BPM.  Please type in a correct BPM.")
title = str(bpmInput) + " BPM playlist"
description = "This is a playlist made by Philip Huang of " + str(bpmInput) + " BPM songs."
new = sp.user_playlist_create(sp.me()['id'], title, True, False, description)
sp.playlist_add_items(new['id'], speed[bpmInput])
print("We have created your playlist.  Have fun running!")
# Plotting out speed data
# speedLen = []
# for array in speed.values():
#     speedLen.append(len(array))
# beatsPerMinute = list(speed.keys())
# fig = plt.figure(figsize=(10, 5))
# plt.bar(beatsPerMinute, speedLen, color='maroon', width=0.4)
# plt.xlabel("Beats per Minutes")
# plt.ylabel("Number of songs")
# plt.title("Songs in your playlist by BPM")
# plt.show()

# one = results['items'][1]['track']['uri']
# one = sp.audio_features(one)
# one = one[0]['tempo']
# # the tempo point is the bpm of the song
# print(json.dumps(one, sort_keys=True, indent=4))
# print(json.dumps(results, sort_keys=True, indent=4))
# check = sp.current_user_playlists()
# for idx, item in enumerate(check['items']):
#     name = item["name"]
#     print(idx, name)
# print(json.dumps(user, sort_keys=True, indent=4))
# check = check["items"]
# print(json.dumps(check, sort_keys=True, indent=4))
# print(check[0]["name"])

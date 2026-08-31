import requests
from bs4 import BeautifulSoup
from ytmusicapi import YTMusic

api_key = "AIzaSyBu-q6ZQJc49NooteAVUWMtqXcig7pXBbY"

date = input("Which date do you want to go back? Use YYYY-MM-DD format.\n")

request = requests.get(f"https://appbrewery.github.io/bakeboard-hot-100/{date}/")
text = request.text

soup = BeautifulSoup(text, "html.parser")
title_tags = soup.select("h3.chart-entry__title")
titles = [title.text for title in title_tags]
print(titles)

yt_music = YTMusic("browser.json")
playlists = yt_music.get_library_playlists()
print(f"Found {len(playlists)} playlists in your library.")

print(playlists)
name = f"{date} Billboard 100"
description = "Billboard 100"
if all([playlist["title"] != name for playlist in playlists]):
    playlist_id = yt_music.create_playlist(name, description)
else:
    playlist = next(filter(lambda playlist: playlist["title"] == name, playlists), None)
    playlist_id = playlist["playlistId"]
    print(playlist_id)

songs = []
for title in titles:
    results = yt_music.search(query=title, filter="songs")
    song = results[0]
    songs.append(song["videoId"])

yt_music.add_playlist_items(playlist_id, songs)

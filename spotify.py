import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
from confidential import *
from progress import *
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
from PIL import Image


sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
pl_id = 'spotify:playlist:0xBYY3VdyBcvqT9i4PLuQX' # Open Test Playlist
offset = 0
artists_dictn = {}
# https://open.spotify.com/playlist/4RuhBX5ngl8b6rG29rKCij?si=d4611193f2ec490d <- starred

while True:
    # Load a batch of 100 songs each iteration
    response = sp.playlist_items(pl_id,
                                 offset=offset,
                                 fields='items.track.id,total',
                                 additional_types=['track'])

    if len(response['items']) == 0:
        
        break

    for count,item in enumerate(response['items']):
        # Loop over all songs
        
        song_id = item["track"]["id"]
        
        if song_id != None:
            
            for artist in sp.track("spotify:track:"+song_id)["artists"]:
                # Loop over artist that contributed to the song
                
                artist_name = artist["name"]
                artists_dictn[artist_name] = artists_dictn[artist_name] +1 if artist_name in artists_dictn else 1   
                    
            report_progress(offset+count, response["total"]-1)
        
    offset = offset + len(response['items'])
   
# Make mask for word cloud
x, y = np.ogrid[:1000, :1000]
mask = (x - 500) ** 2 + (y - 500) ** 2 > 400 **2
mask = 255 * mask.astype(int)

# Create empty image
fig, ax = plt.subplots()
fig.set_size_inches(10, 10)

# Create Wordcloud
wordcloud = WordCloud(font_path = 'Spotify-Font.otf', background_color="rgba(255, 255, 255, 0)", colormap="summer", mode="RGBA",width=1920, height=1920, mask = mask, collocations=False).generate_from_frequencies(artists_dictn)
imagebox = OffsetImage(wordcloud, zoom = 0.61)
ab = AnnotationBbox(imagebox, (960, 960), frameon = False)
ax.add_artist(ab)

# Set Background image
plt.imshow(plt.imread('bg_spotify.jpg'), interpolation="bilinear")

# Save Image
plt.axis('off')
plt.savefig('Spotfy_Wordcloud.png')
plt.close()

# Crop Image
im = Image.open("Spotfy_Wordcloud.png")
 
# Setting the points for cropped image
left = 128
top = 128
right = left + 770
bottom = left + 750
 
# Cropped image of above dimension
im1 = im.crop((left, top, right, bottom))
 
# Shows the image in image viewer
im1.save("Spotify_Wordcloud_Cropped.png")
print("Finished")
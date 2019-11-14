# Spotify Album art viewer
# Charlie Jindra
# 11/14/2019

# Points to local db and grabs albums from a table to
# generate album covers on an html file.

# Run program, then open albumCovers.html.

# Must also login to spotify using OAuth (just run the program with your name as the first argument)
# example: python spotipyPlusDB.py yourCoolName

#0. import necessary packages
import pymysql
import matplotlib.pyplot as plt # you must have matplotlib installed
import spotipy
import spotipy.util as util
import os, sys
import time
import json
import webbrowser

print('Please select a mode:')
print('(1) simple collage')
print('(2) fancy collage')
print('(3) fancy collage with album caption')
print('(4) fancy collage with artist and album')
mode = input('>')

dimension = input('how big do you want the albums? (answer >50)')

username =  "charlessjindra"
# sys.argv[1]
scope = 'user-modify-playback-state user-top-read playlist-modify-public user-read-currently-playing playlist-read-collaborative'

#erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

spotifyObj = spotipy.Spotify(auth=token)

#1. Connect to the university database
db = pymysql.connect("localhost","root","","music" ) # connecting to the database using pymysql interface.
cursor = db.cursor()

#2. Using pymsql and pandas, execute at least two different 'select' queries. To print a dataframe 'df' of pandas, write 'print(df)'
sql = "SELECT * FROM albums"

#fetch all db data from album table
try:
   cursor.execute(sql)
   results = cursor.fetchall()
except:
   print ("Error: unable to fetch data")

#open html file for writing
html = open("htmlFiles/albumCovers.html", 'w')

#prepare initial html file
html.write("<!DOCTYPE html>\n<html>\n<head>\n<link rel=\"stylesheet\" href=\"styles.css\">\n<link rel=\"stylesheet\" href=\"albumStyle.css\">\n</head>\n<body>")



print("working...")
print("albums missed:")

for entry in results:

   #set album and artist from db data
   artist = entry[1]
   album_name = entry[0]

   #making searching for self titled albums better
   if album_name == '(Self Titled)':
      album_name = artist

   #for readability later
   dimension_int = int(dimension)

   try:
      #print('{} {}'.format(album_name, artist))
      album = spotifyObj.search('{} {}'.format(album_name, artist), limit=1,  type='album')

      #going deeper into album json to be more relevant
      album = album['albums']['items'][0]

      #print(json.dumps(album, indent=4))
      image_url = album['images'][0]['url']
      #print(json.dumps(image_url, indent=4))
      top_length = int((dimension_int/7)-1)
      #print(album_name[0:top_length])

      #print((dimension/11)-2)
      #if name of album is too long then we're cutting it off
      # 11 is the pt of font for captions
      if (len(album_name) > top_length ):
         album_name = album_name[0:top_length]
         album_name = album_name + "..."

      if (len(artist) > top_length ):
         artist = artist[0:top_length]
         artist = artist + "..."

      #write album cover html to albumCovers.html
      if (mode == '1' or mode == '2'):
         html.write("<img src=\"{}\">".format(image_url))
      elif (mode=='3'):
         html.write("<figure style=\"word-wrap:word-break\"><img src=\"{}\"><figcaption>{}</figcaption></figure>".format(image_url, album_name))
      else:
         html.write("<figure style=\"word-wrap:word-break\"><img src=\"{}\"><figcaption>{}<br/>{}</figcaption></figure>".format(image_url, album_name, artist))

   except:
      print("{} by {}".format(album_name, artist))

   #time.sleep(1000)
   
#prepare initial html file
html.write("\n</body>\n</html>")

#open css file for writing
css = open("htmlFiles/albumStyle.css", 'w')
if mode == '1':
   cssPrepare = "img [ width: {}px;height: {}px;] \n ".format(dimension, dimension)
else:
   cssPrepare = "img [ box-shadow: 3px 3px;margin: 3px 3px 3px 3px;width: {}px;height: {}px;] \nfigcaption [ padding: 3px;text-align: center;background-color: #222;width:100; color: white;font-family:sans-serif;font-style:italic;font-size:11px;margin: 2px]".format(dimension, dimension)


cssPrepare = cssPrepare.replace("[", r"{")
cssPrepare = cssPrepare.replace("]", r"}")
css.write(cssPrepare)

webbrowser.open("file://C:/Users/Charlie/Documents/hobbyProjects/python_projects/spotipyPlusDB/htmlFiles/albumCovers.html")
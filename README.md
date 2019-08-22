# Artist All Song On Spotify Retriever

A Python script that searches for an artist and retrieves all of their songs including features and remixes using the Spotify Web API. The Python script returns a list of all the song names and the number of songs the artist has on Spotify. Also the Python script gives you the option of adding all the songs found onto a Spotify playlist of your choosing.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system. 

### Installation

Install all the third-party modules required in the directory where searchScrapper.py are located.

Install spotipy
```
$ sudo pip3 install spotipy
```
### Setup

Create a file called config.py in directory of searchScrapper.py and in that file copy and paste
```
CLIENT_ID = ''
CLIENT_SECRET = ''
```
Login to Spotify for Developers and go to your dashboard and select “create client id” and follow the instructions. Spotify are not too strict on providing permissions so put anything you like when they ask for commercial application. 
Copy/Paste client id and client secret in their respective fields, inside the quotation marks.
```
CLIENT_ID = 'aflsdkjflk'
CLIENT_SECRET = 'lskadjflk'
```
If you want to download the songs onto your playlist go to the commercial application you have created and click on edit settings. 

Under redirect URIs add
```
http://localhost:8888/callback/
```

## Deployment

Navigate to the directory where searchScrapper.py are located in Terminal and change the .py file’s permissions to make it executable

```
$ chmod +x searchScrapper.py
```

To run

```
$ ./searchScrapper.py
```

## Dependencies

* Spotipy - lightweight Python library for the Spotify Web API







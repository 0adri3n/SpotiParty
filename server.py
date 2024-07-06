from flask import Flask
from flask import render_template, url_for, request, flash, redirect, session
import os
import requests
import startupflaskspotify
import yaml
from werkzeug.utils import secure_filename
from sys import platform as _platform
import signal
import sys
import atexit

# SETTING UP DNS RECORD
##############################################################################################################################
# def osFinder():
#     if _platform == "linux":
#         return "/etc/hosts"
#     elif _platform == "darwin":
#         return "/etc/hosts"
#     elif _platform == "win32":
#         return "C:\\Windows\\System32\\drivers\\etc\\hosts"

# from python_hosts import Hosts, HostsEntry
# hosts = Hosts(path=osFinder())
# new_entry = HostsEntry(entry_type='ipv4', address='127.0.0.1', names=['www.spotiparty.com', 'spotiparty'])
# hosts.add([new_entry])
# hosts.write()

# def signal_handler(sig, frame):
#     hosts = Hosts(path=osFinder())
#     hosts.remove_all_matching(name='www.spotiparty.com')
#     hosts.write()
#     sys.exit(0)

# signal.signal(signal.SIGINT, signal_handler)

# def exit_handler():
#     hosts = Hosts(path=osFinder())
#     hosts.remove_all_matching(name='www.spotiparty.com')
#     hosts.write()

# atexit.register(exit_handler)

##############################################################################################################################



app = Flask(__name__)
app.secret_key = "supersecretkey"


ALL_SESSION = {"spotifytoken": "", "spotifyuser": ""}
FIRST_LOAD = True


@app.route('/callback/')
def callback():

    startupflaskspotify.getUserToken(request.args['code'])

    ALL_SESSION['spotifytoken'] = startupflaskspotify.getAccessToken()[0]
    r = requests.get("https://api.spotify.com/v1/me", headers={"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Bearer {}".format(ALL_SESSION["spotifytoken"])})
    r = r.json()
    ALL_SESSION['spotifyuser'] = r['display_name']
    print(ALL_SESSION['spotifyuser'])
    return redirect(url_for('index'))

@app.route('/loginSpotify', methods=["GET"])
def loginSpotify():

    global FIRST_LOAD

    response = startupflaskspotify.getUser()
    print(response)
    FIRST_LOAD = False
    return redirect(response)


@app.route("/add/song", methods=['POST'])
def addSong():

    songlink = request.form["lien"]

    start_index = songlink.find("/track/") + len("/track/")
    end_index = songlink.find("?si=")

    song_uri = "spotify:track:" + songlink[start_index:end_index]


    headers = {
        'Authorization': f'Bearer {ALL_SESSION["spotifytoken"]}',
        'Content-Type': 'application/json',
        "Accept": "application/json",
    }

    url = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks?uris={song_uri}"
    r = requests.post(url, headers=headers)
    response = r.json()

    return redirect(url_for('added'))


@app.route("/added")
def added():

    return render_template("added.html")

@app.route('/index')
def index():


    if FIRST_LOAD:

        return redirect('loginSpotify')

    else:
        
        return render_template("index.html", user=ALL_SESSION["spotifyuser"])

@app.route("/")
def base():

    return redirect("index")

def load_config():

    global PLAYLIST_ID
    global CLIENT_ID
    global SECRET_TOKEN

    with open("config/config.yaml", "r") as conf:
        confData = yaml.safe_load(conf)
        playlist_link = confData['playlist_link']
        CLIENT_ID = confData['client_id']
        SECRET_TOKEN = confData['client_token']

    start_index = playlist_link.find("/playlist/") + len("/playlist/")
    end_index = playlist_link.find("?si=")

    PLAYLIST_ID = playlist_link[start_index:end_index]


if __name__ == '__main__':

    #import logging
    #logging.basicConfig(filename='server.log',level=logging.DEBUG)

    load_config()

    app.run(debug=True, host="0.0.0.0")

from flask_spotify_auth import getAuth, refreshAuth, getToken
import yaml
with open("config/config.yaml", "r") as conf:
    confData = yaml.safe_load(conf)
    local_ip = confData["local_ip"]


#Add your client ID
CLIENT_ID = confData["client_id"]

#aDD YOUR CLIENT SECRET FROM SPOTIFY
CLIENT_SECRET = confData["client_token"]

#Port and callback url can be changed or ledt to localhost:5000
CALLBACK_URL = f"http://{local_ip}:5000"

#Add needed scope from spotify user
SCOPE = "playlist-modify-private"
#token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown 
TOKEN_DATA = []


def getUser():
    return getAuth(CLIENT_ID, "{}/callback/".format(CALLBACK_URL), SCOPE)

def getUserToken(code):
    global TOKEN_DATA
    TOKEN_DATA = getToken(code, CLIENT_ID, CLIENT_SECRET, "{}/callback/".format(CALLBACK_URL))
 
def refreshToken(time):
    time.sleep(time)
    TOKEN_DATA = refreshAuth()

def getAccessToken():
    return TOKEN_DATA

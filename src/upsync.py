import sys
from remote_synchronizer.synchronizer import synchronizer
from remote_synchronizer.onedrive.onedrive_remote_manager import onedrive_remote_manager
import onedrivesdk
import json
import re

params = json.load(open('upsync_conf.json'))

cloud_path_to_sync = params["remote_path_to_sync"]
local_path_to_sync = params["local_path_to_sync"]

client_secret = params["client_secret"]
client_id=params["client_id"]

redirect_uri = 'http://localhost:8080/'

api_base_url='https://api.onedrive.com/v1.0/'
scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

#Client initialisation

http_provider = onedrivesdk.HttpProvider()
auth = onedrivesdk.AuthProvider(
    http_provider=http_provider,
    client_id=client_id,
    scopes=scopes)

should_authenticate_via_browser = False
try:
    # Look for a saved session. If not found, we'll have to 
    # authenticate by opening the browser.
    auth.load_session()
    auth.refresh_token()
except FileNotFoundError as e:
    should_authenticate_via_browser = True
    pass

if should_authenticate_via_browser:
    auth_url = auth.get_auth_url(redirect_uri)
    code = ''
    while not re.match(r'[a-zA-Z0-9_-]+', code):
        # Ask for the code
        print('Paste this URL into your browser, approve the app\'s access.')
        print('Copy the resulting URL and paste it below.')
        print(auth_url)
        code = input('Paste code here: ')
        # Parse code from URL if necessary
        if re.match(r'.*?code=([a-zA-Z0-9_-]+).*', code):
            code = re.sub(r'.*?code=([a-zA-Z0-9_-]*).*', r'\1', code)
    auth.authenticate(code, redirect_uri, client_secret)
    auth.save_session()

client = onedrivesdk.OneDriveClient(api_base_url, auth, http_provider)

# Initialize the remote manager and the synchronizer
remote_manager = onedrive_remote_manager(client)
synchronizer = synchronizer(remote_manager, local_path_to_sync, cloud_path_to_sync)

print("**************************************")
print("Starting Synchronization")
print("local folder : ", local_path_to_sync)
print("remote folder : ", cloud_path_to_sync)
print("**************************************")

#launching sync
synchronizer.Synchronize()

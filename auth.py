# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
from os import mkdir
from os.path import exists, join
import shutil
import spotipy
from spotipy.util import prompt_for_user_token
from xdg import BaseDirectory

auth_dir = BaseDirectory.save_config_path('spotipy')

print("""This script creates the token information needed for running spotify
      with a set of personal developer credentials.

      It requires the user to go to developer.spotify.com and set up a
      developer account, create an "Application" and make sure to whitelist
      "https://localhost:8888".

      After you have done that enter the information when prompted and follow
      the instructions given.
""")

CLIENT_ID = input('YOUR CLIENT ID: ')
CLIENT_SECRET = input('YOUR CLIENT SECRET: ')
USERNAME = input('YOUR USERNAME: ')
REDIRECT_URI = 'https://localhost:8888'
SCOPE = ('user-library-read streaming playlist-read-private user-top-read '
         'user-read-playback-state')

am = prompt_for_user_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                           redirect_uri=REDIRECT_URI, scope=SCOPE,
                           username=USERNAME)

sp = spotipy.Spotify(auth_manager=am)

if not exists(auth_dir):
    mkdir(auth_dir)

shutil.move('.cache-{}'.format(USERNAME), join(auth_dir, 'token'))

choice_valid = False
while not choice_valid:
    choice = input('Do you want to save the Client Secrets? (y/n) ')
    choice_valid = choice.lower() in ('yes', 'y', 'no', 'n')

if choice in ('yes', 'y'):
    info = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
    with open(join(auth_dir, 'auth'), 'w') as f:
        json.dump(info, f)

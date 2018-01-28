import os
from os.path import join, expanduser, lexists

CLIENT_DIR = join(expanduser("~"), ".gcal-quickeradd")
if not lexists(CLIENT_DIR):
    os.makedirs(CLIENT_DIR)

CREDENTIALS_FILE = join(CLIENT_DIR, "gcal-credentials")
CLIENT_SECRET_FILE = join(CLIENT_DIR, 'client_secret.json')

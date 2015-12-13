#!/usr/bin/env python3

import dropbox
import shell
import argparse
from oauth import OAUTH_TOKEN

def list():
    for f in dropbox.files_list_folder('').entries:
        print(f.name)

def up(title, myfile):
    dropbox.files_upload(title, myfile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ls", help="list the files in the current directory")
    args = parser.parse_args()

    try:
        dropbox = dropbox.Dropbox(OAUTH_TOKEN)
    except:
        print("Malformed OAuth 2 access token!")

    if args.ls:
        list()

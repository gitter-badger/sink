#!/usr/bin/env python3

import dropbox
import os
import sys
import shell
import argparse
from oauth import OAUTH_TOKEN

class Sink(object):

    def __init__(self):
        self.dropbox = dropbox.Dropbox(OAUTH_TOKEN)

        self.conf_file = open(os.path.join(os.path.expanduser('~'),'.sink'), "r+")
        self.curdir = "/"
        self.curdir = self.conf_file.readline().rstrip()
        self.conf_file.close()

        parser = argparse.ArgumentParser(
                "Sink: for all your sinking needs",
                usage="todo")
        parser.add_argument("command", help="subcommand")

        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            print("Command not found")
            parser.print_help()
            exit()

        getattr(self, args.command)()
        self.unload()

    def ls(self):
        parser = argparse.ArgumentParser(
                description="List files in the current directory")
        parser.add_argument("dir", nargs="?")
        args = parser.parse_args(sys.argv[2:])

        if args.dir == None: args.dir = self.curdir
        if not args.dir.startswith("/"): args.dir = "/" + args.dir
        if args.dir == "/": args.dir = ""

        for f in self.dropbox.files_list_folder(args.dir).entries:
            print(f.name)

    def cd(self):
        parser = argparse.ArgumentParser(
                description="Change the directory")
        parser.add_argument("dir", nargs="?")
        args = parser.parse_args(sys.argv[2:])

        if args.dir == None: args.dir = "/"

        self.curdir = args.dir

    def upload(self, title, myfile):
        dropbox.files_upload(title, myfile)

    def unload(self):
        self.conf_file = open(os.path.join(os.path.expanduser('~'),'.sink'), "w+")
        self.conf_file.write(self.curdir)
        self.conf_file.close()

if __name__ == "__main__":
    Sink()

# user authorization
#from dropbox import DropboxOAuth2FlowNoRedirect
#
#auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
#
#authorize_url = auth_flow.start()
#print "1. Go to: " + authorize_url
#print "2. Click \"Allow\" (you might have to log in first)."
#print "3. Copy the authorization code."
#auth_code = raw_input("Enter the authorization code here: ").strip()
#
#try:
#    access_token, user_id = auth_flow.finish(auth_code)
#except Exception, e:
#    print('Error: %s' % (e,))
#    return
#
#dbx = Dropbox(access_token)

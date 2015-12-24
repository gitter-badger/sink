#!/usr/bin/env python3

import dropbox
import sys
import shell as sh
import argparse
from oauth import OAUTH_TOKEN

class Sink(object):
    SINK_DIR = "SINK_DIR"

    def init_dropbox(self):
        self.dropbox = dropbox.Dropbox(OAUTH_TOKEN)
    #user authorization
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

    def init_config(self):
        self.conf_file = open(sh.join_paths(sh.get_home_dir(),'.sink'), "r+")
        self.curdir = "/"
        self.curdir = self.conf_file.readline().rstrip()
        #self.curdir = sh.get_var(Sink.SINK_DIR, self.curdir)
        self.conf_file.close()

    def init_args(self):
        self.args = sys.argv[1:]

    def __init__(self):
        self.init_dropbox()
        self.init_config()
        self.init_args()

        parser = argparse.ArgumentParser(
                "Sink: for all your sinking needs",
                usage="todo")
        parser.add_argument("command", help="subcommand")

        args = parser.parse_args(self.args[0:1])

        if not hasattr(self, args.command):
            print("Command not found")
            parser.print_help()
            exit()

        getattr(self, args.command)()
        self.unload()

    def ls(self):
        parser = argparse.ArgumentParser(
                description="List files in the specified directory")
        parser.add_argument("dir", nargs="?", default=self.curdir)
        args = parser.parse_args(self.args[1:])

        if not args.dir.startswith("/"): args.dir = "/" + args.dir
        if args.dir == "/": args.dir = ""

        for f in self.dropbox.files_list_folder(args.dir).entries:
            print(f.name)

    def cd(self):
        parser = argparse.ArgumentParser(
                description="Change the directory")
        parser.add_argument("dir", nargs="?", default="/")
        args = parser.parse_args(self.args[1:])
        self.curdir = args.dir

    def repl(self):
        PROMPT = self.dropbox.users_get_current_account().email + " > "
        parser = argparse.ArgumentParser(
                description="Use the sink repl")
        parser.add_argument("command", help="subcommand")

        while True:
            self.args = input(PROMPT).split(' ')
            args = parser.parse_args(self.args[0:1])
            if not hasattr(self, args.command):
                print("Command not found")
                continue
            getattr(self, args.command)()

    def upload(self, title, myfile):
        dropbox.files_upload(title, myfile)

    def unload(self):
        self.conf_file = open(sh.join_paths(sh.get_home_dir(),'.sink'), "w+")
        self.conf_file.write(self.curdir)
        #sh.set_var(Sink.SINK_DIR, self.curdir)
        self.conf_file.close()
    
    def exit(self):
        exit()

if __name__ == "__main__":
    Sink()


#!/usr/bin/env python3

import dropbox
import sys
import shell as sh
import argparse
import util
from oauth import OAUTH_TOKEN
from termcolor import colored as coloured

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter as word_completer
from prompt_toolkit.history import FileHistory as file_history


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
        self.curdir = self.__sanitize_dir(self.conf_file.readline().rstrip())
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

    def __sanitize_dir(self, dir):
        # dropbox api does not like '/' refering to root dir
        if dir == "/" or dir == "":
            return ""

        if not dir.startswith("/"):
            dir = "/" + dir

        if dir.endswith("/"):
            dir = dir[:-1]
        return dir

    def cwd(self):
        parser = argparse.ArgumentParser(
                description="Display the current working directory")

        print(coloured(self.curdir+"/", 'white'))

    def ls(self):
        parser = argparse.ArgumentParser(
                description="List files in the specified directory")
        parser.add_argument("dir", nargs="?", default=self.curdir)
        args = parser.parse_args(self.args[1:])

        if not args.dir.startswith("/"): args.dir = "/" + args.dir
        if args.dir == "/": args.dir = ""

        for f in self.dropbox.files_list_folder(args.dir).entries:
            if util.is_file(f):
                print(coloured(f.name, 'white'))
            else:
                print(coloured(f.name, 'yellow'))

    def generate_completer(self):
        """Generates the autocompletion listing"""
        return word_completer(list(map(lambda x: x.name,
            self.dropbox.files_list_folder(self.curdir).entries)))
        # filter by directory
        #return word_completer(map(lambda x: x.name,
        #    filter(lambda x: not util.is_file(x),
        #        self.dropbox.files_list_folder(self.curdir).entries)))

    def cd(self):
        parser = argparse.ArgumentParser(
                description="Change the directory")
        parser.add_argument("dir", nargs="?", default="/")
        args = parser.parse_args(self.args[1:])
        self.curdir = self.__sanitize_dir(args.dir)

    def repl(self):
        PROMPT = self.dropbox.users_get_current_account().email + " > "
        parser = argparse.ArgumentParser(
                description="Use the sink repl")
        parser.add_argument("command", help="subcommand")

        while True:
            self.args = prompt(
                    PROMPT,
                    vi_mode=True,
                    completer=self.generate_completer(),
                    history=file_history(sh.join_paths(sh.get_home_dir(), '.sinkhist'))
                    ).split(' ')
            args = parser.parse_args(self.args[0:1])
            if not hasattr(self, args.command):
                print("Command not found")
                continue
            getattr(self, args.command)()

    def upload(self, title, myfile):
        dropbox.files_upload(title, myfile)

    def download(self):
        parser = argparse.ArgumentParser(
                description="Download a file to the directory specified")
        parser.add_argument("file")
        args = parser.parse_args(self.args[1:])
        md, res = dropbox.files_download(args.file)


    def unload(self):
        self.conf_file = open(sh.join_paths(sh.get_home_dir(),'.sink'), "w+")
        self.conf_file.write(self.curdir)
        #sh.set_var(Sink.SINK_DIR, self.curdir)
        self.conf_file.close()
    
    def exit(self):
        exit()

if __name__ == "__main__":
    Sink()


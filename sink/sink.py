#!/usr/bin/env python3

import argparse
import contextlib
import dropbox
import sys
import time
import shell as sh
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
        self.conf_file = open(sh.join_paths(sh.get_home_dir(), '.sink'), "r+")
        self.curdir = util.directory(self.conf_file.readline().rstrip())
        #self.curdir = self.__sanitize_dir(self.conf_file.readline().rstrip())
        #self.curdir = sh.get_var(Sink.SINK_DIR, self.curdir)
        self.conf_file.close()

    def init_args(self):
        self.args = sys.argv[1:]

    def __init__(self):
        self.init_dropbox()
        self.init_config()
        self.init_args()

        parser = argparse.ArgumentParser("Sink: for all your sinking needs",
                                         usage="todo")
        parser.add_argument("command", help="subcommand")

        args = parser.parse_args(self.args[0:1])

        if not hasattr(self, args.command):
            print("Command not found")
            parser.print_help()
            exit()

        getattr(self, args.command)()
        self.__unload()

    def __sanitize_dir(self, dir):
        # dropbox api does not like '/' refering to root dir
        if dir == "/" or dir == "":
            return ""

        if not dir.startswith("/"):
            dir = "/" + dir

        if dir.endswith("/"):
            dir = dir[:-1]
        return dir

    def __sanitize_file(self, file):
        if not file.startswith("/"):
            file = "/" + file
        return file

    def cwd(self):
        self.pwd()

    def pwd(self):
        parser = argparse.ArgumentParser(
            description="Display the current working directory")

        print(coloured(self.curdir.get_dir(), 'white'))

    def ls(self):
        parser = argparse.ArgumentParser(
            description="List files in the specified directory")
        parser.add_argument("dir", nargs="?", default=self.curdir.get_dir())
        args = parser.parse_args(self.args[1:])

        args.dir = self.__sanitize_dir(args.dir)

        try:
            for f in self.dropbox.files_list_folder(args.dir).entries:
                if util.is_file(f):
                    print(coloured(f.name, 'white'))
                else:
                    print(coloured(f.name, 'yellow'))
        except dropbox.exceptions.ApiError as e:
            print(coloured("sink ls: no such directory", "red"))

    def generate_completer(self):
        """Generates the autocompletion listing"""
        return word_completer(list(map(lambda x: x.name,
                                       self.dropbox.files_list_folder(
                                           self.curdir.get_dir()).entries)))
        # filter by directory
        #return word_completer(map(lambda x: x.name,
        #    filter(lambda x: not util.is_file(x),
        #        self.dropbox.files_list_folder(self.curdir).entries)))

    def cd(self):
        parser = argparse.ArgumentParser(description="Change the directory")
        parser.add_argument("dir", nargs="?", default="/")
        args = parser.parse_args(self.args[1:])

        old_dir = self.curdir.get_directory()
        self.curdir.change_directory(args.dir)

        try:
            self.dropbox.files_list_folder(self.curdir.get_dir())
        except dropbox.exceptions.ApiError as e:
            self.curdir = util.directory(old_dir)
            print(coloured("sink cd: no such directory", "red"))

    def repl(self):
        PROMPT = self.dropbox.users_get_current_account().email + " > "
        parser = argparse.ArgumentParser(description="Use the sink repl")
        parser.add_argument("command", help="subcommand")

        while True:
            self.args = prompt(PROMPT,
                               vi_mode=True,
                               completer=self.generate_completer(),
                               history=file_history(sh.join_paths(
                                   sh.get_home_dir(), '.sinkhist'))).split(' ')
            args = parser.parse_args(self.args[0:1])
            if not hasattr(self, args.command):
                print("Command not found")
                continue
            getattr(self, args.command)()

    def upload(self, title, myfile):
        dropbox.files_upload(title, myfile)

    def down(self):
        self.download()

    def download(self):
        """Downloads a file from the user's dropbox"""
        cwd = sh.get_cwd() + "/"
        parser = argparse.ArgumentParser(
            description="Download a file to the directory specified")
        parser.add_argument("file")
        parser.add_argument("dest", nargs="?", default=cwd)
        args = parser.parse_args(self.args[1:])

        with self.stopwatch('download'):
            try:
                dbfile = util.file_path(self.curdir.get_directory(), args.file)
                destfile = util.file_path(args.dest, args.file)

                # user has specified local directory to save
                if not args.dest == cwd:
                    self.dropbox.files_download_to_file(
                        destfile.get_full_path(), dbfile.get_full_path())
                    print(coloured("file (" + dbfile.get_full_path(
                    ) + ") saved locally to " + destfile.get_full_path(),
                                   'green'))
                else:  # default to pwd of where sink was run
                    self.dropbox.files_download_to_file(
                        destfile.get_filename(), dbfile.get_full_path())
                    print(coloured("file (" + dbfile.get_full_path(
                    ) + ") saved locally to current directory " +
                                   destfile.get_full_path(), 'green'))

            except dropbox.exceptions.HttpError as err:
                print(coloured("sink download: could not download file",
                               "red"))
            except dropbox.exceptions.ApiError as err:
                print(coloured("sink download: no such file", "red"))

    @contextlib.contextmanager
    def stopwatch(self, message):
        """Context manager to print how long a block of code took."""
        t0 = time.time()
        try:
            yield
        finally:
            t1 = time.time()
            print('Total elapsed time for %s: %.3f' % (message, t1 - t0))

    def __unload(self):
        self.conf_file = open(sh.join_paths(sh.get_home_dir(), '.sink'), "w+")
        self.conf_file.write(self.curdir)
        #sh.set_var(Sink.SINK_DIR, self.curdir)
        self.conf_file.close()

    def exit(self):
        exit()


if __name__ == "__main__":
    Sink()

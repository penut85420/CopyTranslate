import json
import os
import sys
import time

import pyperclip as pc
from googletrans import Translator


class TranslationHero(Translator):
    def __init__(self, dest='en'):
        Translator.__init__(self)
        self.dest = dest
        try:
            self.get_trans('Test')
        except ValueError:
            print('Error: %s is an invalid destination language.' % self.dest)
            exit(1)
    
    def get_trans(self, s):
        t = self.translate(s, dest=self.dest)
        return t.text


class ClipboardMonitor:
    def __init__(self, update_time=1, destination_language='en', no_first=False):
        self.update_seconds = update_time
        self.dest = destination_language
        self.th = TranslationHero(destination_language)
        self.last = pc.paste() if no_first else str()
        self.now = self.last
        self.origin = str()
        self.trans = str()
        self.pause = False

    def run(self):
        self.pause = False
        print('[Copy Translate]')
        print('Update time: %.1f' % self.update_seconds)
        print('Destination language: %s' % self.th.dest.upper())
        print('Begin translating!')
        try:
            self.monitor()
        except KeyboardInterrupt:
            print('\nBye!')
            exit(0)
        except:
            self.th = TranslationHero(self.dest)

    def iter(self):
        self.now = pc.paste()
        if self.now != self.last and len(self.now.strip()) != 0:
            self.origin = self.preprocessing(self.now)
            print('\n[Origin]\n%s' % self.origin)
            self.trans = self.th.get_trans(self.origin)
            print('[Translation]\n%s' % self.trans)
            self.last = self.now
    
    def monitor(self):
        while not self.pause:
            self.iter()
            time.sleep(self.update_seconds)

    def preprocessing(self, t):
        t = t.replace('\n', ' ')
        t = t.replace('\r', ' ')
        t = t.replace('  ', ' ')
        return t.strip()


class ConfigParser:
    CONFIG_PATH = './copy_translate_config.ini'

    def __init__(self, *args):
        self.gap = 1
        self.dest = 'en'
        self.no_first = False
        self.args = dict()
        self.init_args()
        self.load_config()
        self.parse(*args)
        self.save_config()
    
    def add_args(self, method, cmds):
        for cmd in cmds:
            self.args[cmd] = method

    def init_args(self):
        def set_gap(self, args):
            try:
                self.gap = float(args[1])
            except:
                print('Error: -t must follow by numeric.')
                exit(1)
        
        def set_dest(self, args):
            self.dest = args[1]
        
        def set_no_first(self, args):
            self.no_first = True
        
        def set_first(self, args):
            self.no_first = False

        def get_help(self, *args):
            print('Usage: py translate.py [-t update_time] [-d destination language] [-n]')
            exit(0)
        
        self.add_args(method=set_gap, cmds=['-t', '--update-time'])
        self.add_args(method=set_dest, cmds=['-d', '--destination-lang'])
        self.add_args(method=set_no_first, cmds=['-n', '--no-first'])
        self.add_args(method=set_first, cmds=['-f', '--first'])
        self.add_args(method=get_help, cmds=['-h', '--help'])
    
    def parse(self, *args):
        for i, arg in enumerate(args):
            if self.args.get(arg, None):
                self.args[arg](self, args[i:])

    def load_config(self):
        if os.path.exists(ConfigParser.CONFIG_PATH):
            with open(ConfigParser.CONFIG_PATH, 'r', encoding='UTF-8') as fin:
                self.config = json.load(fin)
                self.gap = self.config['update_time']
                self.dest = self.config['destination_language']
                self.no_first = self.config['no_first']
    
    def save_config(self):
        with open(ConfigParser.CONFIG_PATH, 'w', encoding='UTF-8') as fout:
            self.config = {
                'update_time': self.gap,
                'destination_language': self.dest,
                'no_first': self.no_first
            }
            json.dump(self.config, fout, indent=2)


if __name__ == '__main__':
    ClipboardMonitor(**ConfigParser(*sys.argv).config).run()

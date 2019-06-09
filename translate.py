from googletrans import Translator
import pyperclip as pc
import time
import sys

class TranslationHero(Translator):
    def __init__(self, dest='en'):
        Translator.__init__(self)
        self.dest = dest
        self.get_trans('Test')
    
    def get_trans(self, s):
        t = self.translate(s, dest=self.dest)
        return t.text

class ClipboardMonitor:
    def __init__(self, update_seconds=1, dest='en', no_first=False):
        self.update_seconds = update_seconds
        self.th = TranslationHero(dest)
        self.last = pc.paste() if no_first else str()
        self.now = self.last
        self.origin = str()
        self.trans = str()
        self.pause = False

    def run(self):
        self.pause = False
        print('Begin translating!')
        try:
            self.monitor()
        except KeyboardInterrupt:
            print('Bye!')
            exit(0)

    def iter(self):
        self.now = pc.paste()
        if self.now != self.last and len(self.now.strip()) != 0:
            self.origin = self.preprocessing(self.now)
            print('Origin: %s' % self.origin)
            self.trans = self.th.get_trans(self.origin)
            print('Translation: %s' % self.trans)
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

if __name__ == '__main__':
    i = 0
    gap = 1
    dest = 'en'
    no_first = False
    while i < len(sys.argv):
        if sys.argv[i] == '-t' or sys.argv[i] == '--update-time':
            i += 1
            try:
                gap = float(sys.argv[i])
            except:
                print('Error: -t must follow by numeric.')
                exit(1)
        elif sys.argv[i] == '-d' or sys.argv[i] == '--destination-lang':
            i += 1
            dest = sys.argv[i]
        elif sys.argv[i] == '-h':
            print('Usage: py translate.py [-t update_time] [-d destination language] [-n]')
            exit(0)
        elif sys.argv[i] == '-n':
            no_first = True
        i += 1
    
    try:
        cm = ClipboardMonitor(update_seconds=gap, dest=dest, no_first=no_first)
        cm.run()
    except ValueError:
        print('Error: %s is not a valid destination language.' % dest)
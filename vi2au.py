import os
from sys import argv
from glob import glob
from shutil import move
from logging import (basicConfig, debug, info, warning, DEBUG)

# Adding directory to cache
root = os.path.expanduser('~')
cache_dir = root + '/.cache/video-to-audio'
if not (os.path.exists(cache_dir)):
    os.mkdir(root+'/.cache/video-to-audio')

log_file = os.path.join(cache_dir, 'info.log')

basicConfig(format="%(levelname)s:%(message)s", level=DEBUG, filename=log_file)

class Collector():
    """
    Usage:
    python3 [vi2au.py] [-d DIR [DIR ...]] [-m MEDIA_NAME [MEDIA_NAME ...]] [-o OUTPUT_DIR]
    python3 [vi2au.py] [-d DIR] [-f FORMAT [FORMAT ...]] [-o OUTPUT_DIR]

    Options and arguments (and corresponding environment variables):
        -h, --help                            Show this help message.
        -d DIR [DIR ...]                      Convert specified/all files in a specified directory.
                                            (if none specified => defaults to current directory)
        -f FORMAT [FORMAT ...]                Convert specific format media.
        -m MEDIA_NAME [MEDIA_NAME ...]        Provide media name.
        -o OUTPUT_DIR                         Output directory.
    """
    
    def __init__(self):
        self.clear = ('cls' if os.name == 'nt' else 'clear')
        self.current_dir = os.getcwd()
        self.__formats__ = self.collect_spec('-f', '*')
        self.__files__ = self.collect_spec('-m')
        self.__dirs__ = self.collect_spec('-d')
        self.__outdir__ = self.collect_spec('-o', '~/Downloads')

        self.collection = []
        self._garbage = []

        self.collect_files()
        self.FILES = len(self.collection)

    def __str__(self):
        return str(self.collection)

    def collect_spec(self, spec, non_empty=''):
        """
        Collects specifier arguments from provided sys.argv
        and return list of arguments in given space.

        spec : (string) => ('-f', '-m', '-d', '-o')
        non_empty : (string/char) => if no such spec found, return non empty list [string/char]
        """
        # Collect 'spec' arguments from sys.argv
        collection = []
        if spec in argv:
            for arg in argv[argv.index(spec) + 1:]:
                # Append till next specifier
                if not arg.startswith('-'): 
                    collection.append(arg)
                else:
                    break

        if non_empty and not collection:
            collection.append(non_empty if (non_empty == '*') else os.path.expanduser(non_empty))
        
        return collection

    def _get_files(self, dir):
        # Invalid path
        if not os.path.exists(dir): return

        os.chdir(dir)
        for file_format in self.__formats__:
            for file in glob('*.{}'.format(file_format)):
                self.collection.append(os.path.join(dir, file))

        os.chdir(self.current_dir)
            
    def collect_files(self):
        # Collect specified file(s) in specified dir(s)
        if self.__dirs__ and self.__files__:
            for dir in self.__dirs__:
                for file in self.__files__:
                    self.collection.append(os.path.join(dir, file))

        # Collect all file(s) in specified dir(s)
        elif self.__dirs__:
            for dir in self.__dirs__:
                self._get_files(dir)

        # Collect specified file(s) in current dir(s)
        elif self.__files__:
            for file in self.__files__:
                    self.collection.append(os.path.join(self.current_dir, file))

        # Collect all file(s) in current dir(s)
        elif not self.__dirs__ and ('-d' in argv or '-f' in argv):
            self._get_files(self.current_dir)

    def mov_to_dir(self, audio_dir, ext):
        if not os.path.exists(audio_dir):
            os.mkdir(audio_dir)

        for audio_file in glob('*.{}'.format(ext)):
            os.system(self.clear)
            debug("Moving file '{}' to {}\ ".format(audio_file, audio_dir))
            move(audio_file, audio_dir)

class VideoToMp3(Collector):
    def __init__(self):
        super().__init__()
        os.system(self.clear)
        debug("Files found = {}".format(self.FILES))

    def __str__(self):
        return super().__str__()

    def splitName(self, filename):
        path = os.path.dirname(filename)
        file = os.path.basename(filename)
        filename, extention = os.path.splitext(file)
        return (path, filename, extention)

    def convert(self, out_extention='mp3'):
        for file in self.collection:
            info('Converting file = {}'.format(file))
            path, filename, extention = self.splitName(file)
            debug("{} | {} | {}".format(path, filename, extention))
            command = 'ffmpeg -i "' + file + '" "' + filename+'.'+out_extention + '"'
            debug("command = " + command)
            os.system(command)

        for dir in self.__outdir__:
            debug("Moving {} file(s) to '{}'".format(out_extention, dir))
            self.mov_to_dir(dir, out_extention)


if __name__ == "__main__":
    args = ('-m', '-h', '--help', '-f', '-d', '-o')
    if not any([arg for arg in argv if arg in args]):
        print("Usage: vi2au [-m MEDIA_NAME [MEDIA_NAME ...]]\n")
        print("vi2au: error: You must provide at least one MEDIA_NAME.")
        print("Type vi2au -h or --help to see a list of all options.")

    else:
        converter = VideoToMp3()
        converter.convert()

    if '-h' in argv or '--help' in argv:
        help(VideoToMp3)

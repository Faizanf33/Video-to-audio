import os
from sys import argv
from glob import glob
from shutil import move
from logging import (basicConfig, error, debug, warning, info)

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

class Collector():
    
    def __init__(self):
        self.clear = ('cls' if os.name == 'nt' else 'clear')
        self.current_dir = os.getcwd()
        self.__formats__ = self.collect_spec('-f', True)
        self.__files__ = self.collect_spec('-m')
        self.__dirs__ = self.collect_spec('-d')
        self.__outdir__ = self.collect_spec('-o')

        self.collection = []
        self._garbage = []

        self.collect_files()
        self.FILES = len(self.collection)

    def __str__(self):
        return str(self.collection)

    def collect_spec(self, spec, non_empty = False):
        collection = []
        if spec in argv:
            for arg in argv[argv.index(spec) + 1:]:
                # Append till next specifier
                if not arg.startswith('-'): 
                    collection.append(arg)
                else:
                    break

        if non_empty and not collection:
            collection.append('*')
        
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

    def mov_to_dir(self, audio_dir = 'Audio'):
        if not os.path.exists(audio_dir):
            os.mkdir(audio_dir)

        for mp3File in glob('*.mp3'):
            os.system(clear)
            debug("Moving file '{}' to {}\ ".format(mp3File, audio_dir))
            move(mp3File, audio_dir)

class VideoToMp3(Collector):
    def __init__(self):
        self.collect = Collector()
        os.system(self.collect.clear)

    def __str__(self):
        return str(self.collect)

    # def convert(self, path, filename):
    #     return 

    def convert(self):
        for file in self.collect.collection:
            print(os.path.splitext(file))



if __name__ == "__main__":
    converter = VideoToMp3()
    print(converter.convert())
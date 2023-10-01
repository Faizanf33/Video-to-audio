# Video-to-audio 
 #### *Convert video file(s) to audio*
___
## Requirements:
- __python3x__
- __ffmpeg__

### Install requirements using terminal:
```bash
sudo apt install python3 ffmpeg
```

## Usage:
```bash
cd Video-to-audio/
```
- *Manually* enter file(s) to convert
```bash
python3 vi2au.py -m <file1> <file2> ...
```
- *Auto* convert all files in current/specified directory
```bash
python3 vi2au.py -d
python3 vi2au.py -d <path> <path> ...
```
- Convert specified format, e.g. mp4, webm, mkv
```bash
python3 vi2au.py -f <format>
python3 vi2au.py -f <format> <format> ...
```
- Specify output directory (default = ~/Downloads)
```bash
python3 vi2au.py -o <path>
python3 vi2au.py -o <path> <path> ...
```
____
__Example__
```bash
python3 vi2au.py -m 'file1.mp4' 'file2.webm' '/video/file3.mkv' -o '/music'
python3 vi2au.py -d -o '/music'
python3 vi2au.py -d '/video' -o '/music'
python3 vi2au.py -d -f 'mp4' 'mkv'
```
____
### *Includes:*
* [x] Convert multiple file(s).
* [x] Convert specified format file(s)
* [x] Convert file(s) in multiple directories.
* [x] Seperate directory for audio files.
* [x] Log file for error(s) or reporting.

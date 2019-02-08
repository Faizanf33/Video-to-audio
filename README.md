# Video-to-audio (Convert video file(s) to audio(mp3))
### Forked from 
*__Aditya Sharma__* [adityashrm21](https://github.com/adityashrm21)

## Requirements:
- __Python3x__
- __Ffmpeg__ 
- __Lame__

### Install requirements using terminal:
```bash
$ sudo apt install python3 ffmpeg lame
```

## Usage:
```bash
$ cd Video-to-audio/
```
- *Manually* enter file(s) to convert
```bash
$ python3 video_to_audio.py <file1> <file2> ...
```
- *Auto* convert all files in current/specified directory
```bash
$ python3 video_to_audio.py -a
$ python3 video_to_audio.py -a <path>
```
- Convert specified format, e.g. mp4, webm, mkv
```bash
$ python3 video_to_audio.py -f <format>
```
__Example__
```bash
$ python3 video_to_audio.py 'file1.mp4' 'file2.webm' '/video/file3.mkv'
$ python3 video_to_audio.py -a 
$ python3 video_to_audio.py -a '/video'
$ python3 video_to_audio.py -f 'mp4'
```

## Includes:
* [x] Convert multiple file(s).
* [x] Convert specified format file(s)
* [x] Seperate directory for audio files.
* [x] Log file for error(s) or reporting.

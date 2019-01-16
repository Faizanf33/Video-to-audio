# import urllib.request
# import urllib.error
# import re
import sys
import time
import os
import pipes
import logging
import glob
import shutil

clear = ('cls' if os.name == 'nt' else 'clear')

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG, filename='info.log')

def video_to_audio(fileName):
	try:
		os.system(clear)
		file, file_extension = os.path.splitext(fileName)
		logging.info("Filename split to {} and {}".format(file, file_extension))
		file = pipes.quote(file)
		video_to_wav = 'ffmpeg -i ' + file + file_extension + ' ' + file + '.wav'
		logging.info("Converting to = {}".format(file[1:-1] + '.wav'))
		os.system(video_to_wav)

		os.system(clear)
		final_audio = 'lame '+ file + '.wav' + ' ' + file + '.mp3'
		logging.info("Final output filename = {}".format(file[1:-1] + '.mp3'))
		os.system(final_audio)

		os.system(clear)
		file = file[1:-1] + '.wav'
		logging.debug("Removing file '{}'".format(file))
		os.remove(file)
		logging.info("Sucessfully converted '{}' into audio!".format(fileName))
		return True

	except Exception as err:
		logging.error("During conversion an error occurred => {}".format(err))
		logging.info("File not converted -> {}".format(fileName))
		pass

	return False

def main():
	file_count = 0
	if len(sys.argv) > 1:
		if (len(sys.argv) == 2) and (sys.argv[1] == '-a'):
			files = os.listdir()

		else:
			files = sys.argv[1:]

		logging.info("File(s) to convert : {}".format(files))
		time.sleep(0.01)

		for filePath in files:
			# check if the specified file exists or not
			try:
				if os.path.exists(filePath):
					logging.info("File received and path exists = {}".format(filePath))

			except OSError as err:
				logging.error("File found but no such path exists = {}".format(filePath))
				pass

			# convert video to audio
			logging.info("Sending file for conversion to procedure '{}'".format(video_to_audio))
			if video_to_audio(filePath):
				file_count += 1
			time.sleep(1)

	else:
		print("""command usage:
	manually => 'python3 video_to_audio.py <file1> <file2> ...'
	auto_all => 'python3 video_to_audio.py -a'
			""")
		return 0

	logging.info("Files converted = {}".format(file_count))
	return file_count

def mov_to_dir(audio_dir = 'Audio'):
	try:
		os.mkdir(audio_dir)
	except:
		pass

	for mp3File in glob.glob('*.mp3'):
		os.system(clear)
		logging.info("Moving file '{}' to {}\ ".format(mp3File, audio_dir))
		shutil.move(mp3File, 'Audio')

	return

# install ffmpeg and/or lame if you get an error saying that the program is currently not installed
if __name__ == '__main__':
	file_count = main()

	if file_count > 0:
		mov_to_dir()	# defaults to Audio\
		# if .wav file(s) not removed
		for file in glob.glob('*.wav'):
			os.remove(file)

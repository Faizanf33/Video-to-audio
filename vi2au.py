import os
import sys
import pipes
import logging
from glob import glob
from shutil import move


clear = ('cls' if os.name == 'nt' else 'clear')

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG, filename='info.log')

def video_to_audio(fileName):
	"""
	Usage:
	python3 [vi2au.py] [-d DIR] [-m MEDIA_NAME [MEDIA_NAME ...]] [-o OUTPUT_DIR]
	python3 [vi2au.py] [-d DIR] [-f FORMAT] [-o OUTPUT_DIR]

	Options and arguments (and corresponding environment variables):
	  -h, --help		Show this help message.
	  -m MEDIA_NAME [MEDIA_NAME ...]		Provide media name.
	  -d DIR		Convert all files in a directory.
					(if none specified => defaults to current directory)
	  -o OUTPUT_DIR		Output directory.
	  -f FORMAT		Convert specific format media.

	"""
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
		logging.info("File not converted/removed -> {}".format(fileName))
		pass

	return False

def main():
	file_count = 0
	files = []
	if ('-d' in sys.argv):
		i = sys.argv.index('-d')
		os.chdir(sys.argv[i + 1]) if os.path.exists(sys.argv[i + 1]) else os.getcwd()

	if ('-m' in sys.argv):
		i = sys.argv.index('-m')
		for arg in sys.argv[i + 1:]:
			if not arg.startswith('-'):
				files.append(arg)
			else:
				break

	if ('-f' in sys.argv):
		i = sys.argv.index('-f')
		for arg in sys.argv[i + 1:]:
			if not arg.startswith('-'):
				for file in glob('*.{}'.format(arg)):
					files.append(file)
			else:
				break

	if not files:
		for file in os.listdir():
			if os.path.isfile(os.path.join(os.getcwd(), file)):
				files.append(file)

	logging.info("Total file(s) to convert : {}".format(len(files)))
	logging.info("File(s) to convert : {}".format(files))

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

	logging.info("Files converted = {}".format(file_count))
	return file_count

def mov_to_dir(audio_dir):
	if not os.path.exists(os.path.join(os.getcwd(), audio_dir)):
		os.mkdir(audio_dir)

	for mp3File in glob('*.mp3'):
		os.system(clear)
		logging.info("Moving file '{}' to {}\ ".format(mp3File, audio_dir))
		move(mp3File, audio_dir)

	return

# install ffmpeg and/or lame if you get an error saying that the program is currently not installed
if __name__ == '__main__':
	if '-h' in sys.argv:
		help(video_to_audio)
		exit()

	try:
		file_count = main()
		if file_count > 0:
			output_dir = 'Audio'
			if '-o' in sys.argv:
				i = sys.argv.index('-o')
				output_dir = sys.argv[i + 1]

			mov_to_dir(output_dir)
			# if .wav file(s) not removed
			for file in glob('*.wav'):
				os.remove(file)

	except Exception as exp:
		print(exp)
		help(video_to_audio)

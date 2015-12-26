#!/usr/bin/env python

import os, sys, ConfigParser, argparse
from PIL import Image
import re



def get_thumb_rect(img_width, img_height, ratio=float(16)/float(9)):
	if img_width*(1/ratio) >= img_height:
		width 	= img_height*ratio
		height 	= img_height
		top = 0
		left = (img_width - width) / 2
	else:
		width 	= img_width
		height 	= img_width*(1/ratio)
		left = 0
		top = (img_height - height) / 2

	return (int(left), int(top), int(left+width), int(top+height))

def resize_to_width(max_width, img_width, img_height):
	if max_width < img_width:
		return (int(max_width), int(img_height*(max_width/img_width)))
	else:
		return (int(img_width), int(img_height))


def read_args(argv):
	parser = argparse.ArgumentParser(epilog=get_usage_epilog(), formatter_class=argparse.RawTextHelpFormatter)
	
	# List of files or directories
	# TODO: add directory support
	parser.add_argument("file", nargs="+", help="Relative path to a JPEG file.")

	# Thumbnail ratio (e. g. 16:9)
	parser.add_argument("-i", "--ratio", dest="ratio", help="Ratio of thumbnail (e. g. \"16:9\")")

	# Thumbnail ratio (e. g. 16:9)
	parser.add_argument("-w", "--max-width", dest="max_width", help="Max thumbnail width in pixels.", type=int)

	# Thumbnail ratio (e. g. 16:9)
	parser.add_argument("-e", "--max-height", dest="max_height", help="Max thumbnail width in pixels.", type=int)

	# Output directory
	parser.add_argument("-o", "--output-dir", dest="out_dir", help="Directory where thumbnails will be stored.", required=True)
	
	# TODO: Zoom argument (in percents, 100 is maximum rectangle)
	# TODO: validate arguments and eventually print error and return None
	return parser.parse_args()


def get_usage_epilog():
	return """
# TODO...
"""


def main(argv):
	args = read_args(argv)

	if args.ratio is None:
		args.ratio = "16:9"

	for in_file in args.file:
		print "[Info] Reading {}".format(in_file)
		file, ext = os.path.splitext(in_file)
		try:
			img 		= Image.open(in_file)
			img_width 	= img.size[0]
			img_height 	= img.size[1]
		except:
			print "[Error] Couldnt't process {}".format(in_file)
			continue

		# Get thumbnail rectangle
		rect = get_thumb_rect(img_width, img_height)

		# Crop
		img = img.crop(rect)
		
		# Resize
		if args.max_width is not None:
			size = resize_to_width(args.max_width, img_width, img_height)
			img = img.thumbnail(size, Image.ANTIALIAS)
			print img.size

		# Save
		img.save(os.path.join(args.out_dir, os.path.basename(in_file)), "JPEG")
		print "[Success] processing {}".format(in_file)



if __name__ == "__main__":
	main(sys.argv[1:])
	
	
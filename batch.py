import os
from os.path import join
from argparse import ArgumentParser
import cv2

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.graphics import renderPDF, renderPM
from reportlab.graphics.shapes import *
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg

def parse_args():
    
    parser = ArgumentParser()
    parser.add_argument('src_dir')
    parser.add_argument('dst_dir')

    args = parser.parse_args()
    return args.src_dir, args.dst_dir

def main():

	src_dir, dst_dir = parse_args()

	src_subdir = os.listdir(src_dir)

	for subdir in src_subdir:
		if not os.path.isdir(join(dst_dir, subdir)):
			os.mkdir(join(dst_dir, subdir))

		src_subfiles = os.listdir(join(src_dir, subdir))

		for subfile in src_subfiles:
			
			#convert rgba to rgb
			im_rgba = cv2.imread(join(src_dir, subdir, subfile), cv2.IMREAD_UNCHANGED)
			im_rgba = im_rgba/255.

			im_rgb = im_rgba[:, :, :3]
			im_rgb[:, :, 0] = im_rgba[:,:, 0] * im_rgba[:,:, 3] + (1-im_rgba[:,:, 3]) * 1
			im_rgb[:, :, 1] = im_rgba[:,:, 1] * im_rgba[:,:, 3] + (1-im_rgba[:,:, 3]) * 1
			im_rgb[:, :, 2] = im_rgba[:,:, 2] * im_rgba[:,:, 3] + (1-im_rgba[:,:, 3]) * 1
			
			tmp_file = "tmp.png"
			cv2.imwrite(tmp_file, im_rgb*255)

			#call color trace
			python = "python36"
			trace_exe = "color_trace_multi.py"
			command_args = [python, trace_exe, "-i", tmp_file, "-o", join(dst_dir, subdir, subfile[:-4]+".svg"), "-c", "10", "-v", "-s"]
			command_str = " ".join(command_args)
			os.system(command_str)


def main_convert_rgba2rgb():

	src_dir, dst_dir = parse_args()

	src_subdir = os.listdir(src_dir)

	for subdir in src_subdir:
		if not os.path.isdir(join(dst_dir, subdir)):
			os.mkdir(join(dst_dir, subdir))

		src_subfiles = os.listdir(join(src_dir, subdir))

		for subfile in src_subfiles:
			
			#convert rgba to rgb
			im_rgba = cv2.imread(join(src_dir, subdir, subfile), cv2.IMREAD_UNCHANGED)
			im_rgba = im_rgba/255.

			im_rgb = im_rgba[:, :, :3]
			im_rgb[:, :, 0] = im_rgba[:,:, 0] * im_rgba[:,:, 3] + (1-im_rgba[:,:, 3]) * 1
			im_rgb[:, :, 1] = im_rgba[:,:, 1] * im_rgba[:,:, 3] + (1-im_rgba[:,:, 3]) * 1
			im_rgb[:, :, 2] = im_rgba[:,:, 2] * im_rgba[:,:, 3] + (1-im_rgba[:,:, 3]) * 1
			
			# tmp_file = "tmp.png"
			cv2.imwrite(join(dst_dir, subdir, subfile), im_rgb*255)


def add_svg(file, canvas, x, y):
	drawing = svg2rlg(file)
	# print(drawing.width)
	# print(drawing.height)
	renderPDF.draw(drawing, canvas, x, y)
def add_png(file, canvas, x, y):
	print(file)
	drawing = Drawing(20, 20)
	img = Image(0,0,20,20, file)
	drawing.add(img)
	renderPDF.draw(drawing, canvas, x, y)
def main_combine():

	my_canvas = canvas.Canvas('svg_on_canvas.pdf')
	num = 0
	src_dir, dst_dir = parse_args()

	src_subdir = os.listdir(dst_dir)

	for subdir in src_subdir:
		
		src_subfiles = os.listdir(join(dst_dir, subdir))

		for subfile in src_subfiles:
			x = (num %10) * 60
			y = (num /10) * 32 - 3*(num%10)
			print(subfile)
			add_png(join(src_dir, subdir, subfile[:-4]+".png"), my_canvas, x, y)
			x += 25
			add_svg(join(dst_dir, subdir, subfile), my_canvas, x, y)
			num+=1

	my_canvas.save()



if __name__ == '__main__':
	
	main_combine()
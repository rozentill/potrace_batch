import os
from os.path import join
from argparse import ArgumentParser
import cv2
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.graphics import renderPDF, renderPM
from reportlab.graphics.shapes import *
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg

def parse_args():
    
    parser = ArgumentParser()
    parser.add_argument('--src_dir')
    parser.add_argument('--dst_dir')
    parser.add_argument('--dst2_dir', required=False)
    args = parser.parse_args()
    return args

def main():

	args = parse_args()

	src_dir = args.src_dir
	dst_dir = args.dst_dir

	src_subdir = os.listdir(src_dir)

	for subdir in src_subdir:
		if not os.path.isdir(join(dst_dir, subdir)):
			os.mkdir(join(dst_dir, subdir))

		src_subfiles = os.listdir(join(src_dir, subdir))

		for subfile in src_subfiles:
			if not (subfile[-3:] == 'png' or subfile[-3:] == 'jpg'):
				continue
			#convert rgba to rgb
			im_rgba = cv2.imread(join(src_dir, subdir, subfile), cv2.IMREAD_UNCHANGED)

			im_rgba = im_rgba/255.
			if len(im_rgba.shape) == 2:
				im_rgba = np.expand_dims(im_rgba, axis=2)
				im_rgb = np.concatenate((im_rgba, im_rgba, im_rgba),axis=2)
			elif im_rgba.shape[2] == 4:
				im_rgb = im_rgba[:, :, :3]
				im_rgb[:, :, 0] = im_rgba[:,:, 0] * im_rgba[:,:, 3] + (1-im_rgba[:,:, 3]) * 1
				im_rgb[:, :, 1] = im_rgba[:,:, 1] * im_rgba[:,:, 3] + (1-im_rgba[:,:, 3]) * 1
				im_rgb[:, :, 2] = im_rgba[:,:, 2] * im_rgba[:,:, 3] + (1-im_rgba[:,:, 3]) * 1
			elif im_rgba.shape[2] == 3:
				im_rgb=im_rgba

			h = im_rgb.shape[0]
			w = im_rgb.shape[1]
			c = im_rgb.shape[2]
			im_rgb_pad = np.ones((h+4, w+4, c))
			im_rgb_pad[2:h+2, 2:w+2, :] = im_rgb

			tmp_file = "tmp.png"
			cv2.imwrite(tmp_file, im_rgb_pad*255)

			#call color trace
			python = "python36"
			trace_exe = "color_trace_multi.py"
			command_args = [python, trace_exe, "-i", "\"%s\""%tmp_file, "-o", "\"%s\""%join(dst_dir, subdir, subfile[:-4]+".svg"), "-c", "10", "-v", "-s"]# -c 0 for grey image, 10 for rgb image
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


def add_svg(file, canvas, x, y, sx, sy):
	drawing = svg2rlg(file)
	drawing.width = 20
	drawing.height = 20
	drawing.scale(sx, sy)
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
	my_canvas.setPageSize((600, 125))
	num = 0
	src_dir, dst_dir = parse_args()

	src_subdir = os.listdir(dst_dir)

	for subdir in src_subdir:
		
		src_subfiles = os.listdir(join(dst_dir, subdir))

		for subfile in src_subfiles:
			x = (num %10) * 60
			y = (num /10) * 32 - 3*(num%10)
			print(subfile)
			f_img = join(src_dir, subdir, subfile[:-4]+".png")
			img = cv2.imread(f_img)
			ox = img.shape[1]
			oy = img.shape[0]
			sx = 20./ox
			sy = 20./oy
			add_png(f_img, my_canvas, x, y)
			x += 25
			add_svg(join(dst_dir, subdir, subfile), my_canvas, x, y, sx, sy)
			num+=1

	my_canvas.save()

def main_combine_two():

	my_canvas = canvas.Canvas('svg_on_canvas.pdf')
	my_canvas.setPageSize((450, 230))
	num = 0
	args = parse_args()
	src_dir = args.src_dir
	dst_dir = args.dst_dir
	dst2_dir = args.dst2_dir

	dst_subdir = os.listdir(dst_dir)

	for subdir in dst_subdir:
		
		src_subfiles = os.listdir(join(dst_dir, subdir))

		for subfile in src_subfiles:

			# if subfile[-4:] is not ".svg":
			# 	continue

			print(subfile)
			x = (num % 5) * 90
			y = (num / 5) * 32 - 6*(num%5)

			f_img = join(src_dir, subdir, subfile[:-4]+".png")

			img = cv2.imread(f_img)

			ox = img.shape[1]
			oy = img.shape[0]

			sx = 16./ox
			sy = 16./oy

			add_png(f_img, my_canvas, x, y)

			x += 25

			add_svg(join(dst_dir, subdir, subfile), my_canvas, x, y-1, sx, sy)# 

			x += 25

			sx = 20./ox
			sy = 20./oy

			add_svg(join(dst2_dir, subdir, subfile), my_canvas, x, y-1, sx, sy)# 

			num+=1

	my_canvas.save()



if __name__ == '__main__':
	
	main_combine_two()
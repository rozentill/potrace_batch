import numpy as np
import cv2

def main():

	in_file = "input/test/001-basket-4.png"
	im_rgba = cv2.imread(in_file, cv2.IMREAD_UNCHANGED)
	im_rgba = im_rgba/255.
	im_rgb = im_rgba[:, :, :3]
	print(im_rgba.max())
	im_rgb[:, :, 0] = im_rgba[:,:, 0] * im_rgba[:,:, 3] + (1-im_rgba[:,:, 3]) * 1
	im_rgb[:, :, 1] = im_rgba[:,:, 1] * im_rgba[:,:, 3] + (1-im_rgba[:,:, 3]) * 1
	im_rgb[:, :, 2] = im_rgba[:,:, 2] * im_rgba[:,:, 3] + (1-im_rgba[:,:, 3]) * 1
	# im_rgb = cv2.cvtColor(im_rgba, cv2.COLOR_RGBA2RGB)
	out_file = "output/test.png"
	cv2.imwrite(out_file, im_rgb*255.)
if __name__ == '__main__':
	main()
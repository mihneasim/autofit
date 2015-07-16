""" Simple geometry for resizing and cropping """
from fractions import gcd

from PIL import Image


def max_bounds(src_w, src_h, ratio_w, ratio_h):
	"""
	Given an area src_w x src_h, determine the maximum area
	of ratio ratio_w:ratio_h which we can fit inside the original area

	"""
	raise NotImplemented


def resize_for(src_w, src_h, dest_w, dest_h):
	"""
	Return the size of the destination image which is about to be used
	for cropping to dest_w, dest_h

	"""
	ratio_cmp = (float(src_w) / src_h) / (float(dest_w) / dest_h)

	if ratio_cmp > 1:
		# source has smaller h than required
		target_h = dest_h
		target_w = int(float(target_h) * src_w / src_h)
	elif ratio_cmp < 1:
		# source has smaller w than required
		target_w = dest_w
		target_h = float(target_w) * src_h / src_w
	else:
		target_w = dest_w
		target_h = dest_h
	return (int(target_w), int(target_h))


def center_crop(src_w, src_h, dest_w, dest_h):
	"""
	Return the 4-tuple box required for center cropping to dest_w, dest_h

	This method requires pre-prepared sizes with max_bouds

	"""
	if src_w == dest_w:
		# crop height
		dy = int((src_h - dest_h) / 2.0)
		return (0, dy, dest_w, dy + dest_h)
	elif src_h == dest_h:
		dx = int((src_w - dest_w) / 2.0)
		return (dx, 0, dx + dest_w, dest_h)
	else:
		raise ValueError("Either height or width should match. Use resize_for")


def autofit(image, dest_w, dest_h):
	"""
	Resize and center crop image to dest_w, dest_h

	image is PIL.Image object, so is returned value

	"""
	resize_w, resize_h = resize_for(image.size[0], image.size[1],
			dest_w, dest_h)
	out = image.resize((resize_w, resize_h), Image.ANTIALIAS)
	return out.crop(center_crop(resize_w, resize_h, dest_w, dest_h))


def guess_ratio(width, height):
	""" Guess w:h ration (divide width and height by greatest com. divisor """
	assert isinstance(width, int)
	assert isinstance(height, int)
	denom = gcd(width, height)
	return "%d:%d" % (width / denom, height / denom)


def ratio2float(ratio):
	""" Converts '16:9' to 1.7777777 """
	w, h = ratio.split(':')
	return float(w) / float(h)

""" Simple geometry for resizing and cropping """
from fractions import gcd
import os

import numpy
from PIL import Image


def max_bounds(dest_w, dest_h, ratio_w, ratio_h):
    """
    Given an area dest_w x dest_h, determine the 2 points (top left,
    bottom right) of the rectangle
    that fits in. Rectangle keeps ratio_w:ratio_h

    returns (x0, y0, x1, y1)

    """
    dest_ratio = dest_w / float(dest_h)
    input_ratio = ratio_w / float(ratio_h)

    if dest_ratio > input_ratio:
        # target height is dest_h
        target_h = dest_h
        target_w = int(round(target_h * float(ratio_w) / ratio_h))
    else:
        target_w = dest_w
        target_h = int(round(target_w * float(ratio_h) / ratio_w))

    dx = int(round((dest_w - target_w) / 2.0))
    dy = int(round((dest_h - target_h) / 2.0))

    return (dx, dy, dx + target_w, dy + target_h)


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

    This method requires pre-prepared sizes with resize_for

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


def autofit_crop(image, dest_w, dest_h):
    """
    Resize and center crop image to dest_w, dest_h

    image is PIL.Image object, so is returned value

    """
    resize_w, resize_h = resize_for(image.size[0], image.size[1],
            dest_w, dest_h)
    out = image.resize((resize_w, resize_h), Image.ANTIALIAS)
    return out.crop(center_crop(resize_w, resize_h, dest_w, dest_h))


def autofit_fill(image, dest_w, dest_h, fill=None):
    """
    Resize and center image to max bounds
    If ratios are different, fill with `fill` (default None, transparency)

    image is PIL.Image object, so is returned value

    """
    x0, y0, x1, y1 = max_bounds(dest_w, dest_h, image.size[0], image.size[1])

    if fill is None:
        fill_color = (255, 255, 255, 0) # transparency
    else:
        fill_color = fill + (255, ) # solid

    canvas = Image.new(mode='RGBA', size=(dest_w, dest_h), color=fill_color)
    canvas.paste(image.resize((x1 - x0, y1 - y0), Image.ANTIALIAS), (x0, y0))

    return canvas


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


def read_gif(filename, as_numpy=True):
    """
    Read images from an animated GIF file. Return a list of numpy
    arrays, or, if as_numpy is false, a list if PIL images.
        Adapted from (C) 2012, Almar Klein, Ant1, Marius van Voorden,
        code subject to the (new) BSD license

    """
    if not os.path.isfile(filename):
        raise IOError('File not found: %s' % filename)

    pil_im = Image.open(filename)
    pil_im.seek(0)

    # Read all images inside
    images = []
    try:
        while True:
            # Get image as numpy array
            tmp = pil_im.convert()  # Make without palette
            a = numpy.asarray(tmp)
            if not a.shape:
                raise MemoryError("Too little memory to convert PIL image to array")
            # Store, and next
            images.append(a)
            pil_im.seek(pil_im.tell() + 1)
    except EOFError:
        pass

    # Convert to normal PIL images if needed
    if not as_numpy:
        return [Image.fromarray(im) for im in images]
    else:
        return images

#def resize_file(filepath, width, height):
    #""" facade for static formats + gif. Return path to actual file """
    #assert os.path.isfile(filepath)
    #fmt = filepath.endswith('.gif') and 'GIF' or 'PNG'

    #if fmt == 'GIF':
        #frames = read_gif(filepath, False)
    #else:
        #frames = [Image.open(filepath)]

    #outs = []
    #for frame in frames:
        #outs.append(autofit_fill(frame, int(width), int(height)))

    #if fmt == 'GIF':
        #tempf = NamedTemporaryFile('wb', suffix='.resize.gif', delete=False)
        #tempf_final_resized = tempf.name
        #resized_frames = []
        #for ind, frame in enumerate(outs):
            #tempframe = NamedTemporaryFile('wb', suffix='gif.frame.%d.png' % ind, delete=False)
            #frame.save(tempframe, 'PNG', quality=95)
            #logger.info("exported frame %s", tempframe.name)
            #resized_frames.append(tempframe.name)
            #tempframe.close()
        #merge_cmd = ['convert', '-dispose', 'none', '-delay', '50', # TODO use source gif period
                     #'-loop', '0'] + resized_frames + [tempf_final_resized]
        #process = Popen(merge_cmd)
    #else:
        #tempf = NamedTemporaryFile('wb', suffix='.resize.png', delete=False)
        #tempf_final_resized = tempf.name
        #outs[0].save(tempf, fmt, quality=95)
    #tempf.close()

    #return tempf_final_resized

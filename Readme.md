AutoFit
=============

The missing crop/frame tools in [PIL](http://www.pythonware.com/products/pil).

What it does
+++++++++++++++
It resizes and crops any image to any size. Yes, it cuts out stuff, or fills
in with transparency/solid colour.

How to use
++++++++++++++

    from PIL import Image
    import autofit

    lolcat = Image.open('lolcat.jpg')
    # center crop, cut out strips left/right or top/bottom to keep ratio
    output = autofit.autofit_crop(lolcat, 640, 640)
    # center image, fill with transparency left/right or top/bottom
    output = autofit.autofit_fill(lolcat, 640, 640)
    # or maybe with solid red
    output = autofit.autofit_fill(lolcat, 640, 640, fill=(255, 0, 0))
    output.save()
    # GIFs don't scare us
    new_file = autofit.resize_file('loops.gif', 100, 100)

AutoFit
=============

The missing crop function in [PIL](http://www.pythonware.com/products/pil).

What it does
+++++++++++++++
It resizes and crops any image to any size. Yes, it cuts out stuff.

How to use
++++++++++++++

    from PIL import Image
    import autofit

    lolcat = Image.open('lolcat.jpg')
    output = autofit.autofit_crop(lolcat, 640, 640)
    output.save()

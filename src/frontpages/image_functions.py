from pathlib import Path

from exif import Image as eI
from loguru import logger
from PIL import Image

from frontpages import file_functions


def pngConvert(abspath):
    """
    Convert all .png in absolute path 'abspath' to .jpg
    """

    newtmp = Path(abspath)

    f = sorted(newtmp.rglob("*.png"))

    for infile in f:
        # construct outfile replace .png extension to .jpg
        outfile = infile.with_suffix(".jpg")
        if infile != outfile:
            try:
                with Image.open(infile) as im:
                    rgb_im = im.convert("RGB")
                    rgb_im.save(outfile, quality=95)
            except OSError:
                logger.error("cannot convert", infile)


def jpgDatetime(abspath, dt_string):
    """
    read list of .jpg, outfile = infile, rename infile .jpg_original
    Update exif data for all .jpg in absolute path 'abspath'.
    """

    newtmp = Path(abspath)

    f = sorted(newtmp.rglob("*.jpg"))

    for infile in f:
        # construct outfile replace .png extension to .jpg
        #  outfile = infile.stem + "-modified" + ".jpg"
        #  outfile = 'newfile.jpg'
        outfile = infile
        try:
            with open(infile, "rb") as image_file:
                file_functions.rename_all4(infile, "_original")
                my_image = eI(image_file)
                my_image.datetime_original = dt_string
            with open(outfile, "wb") as new_image_file:
                new_image_file.write(my_image.get_file())
        except OSError:
            logger.error("cannot convert", infile)

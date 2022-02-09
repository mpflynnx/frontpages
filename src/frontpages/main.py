import sys
from datetime import date, datetime
from pathlib import Path

import click
from loguru import logger

from frontpages import __version__, file_functions, image_functions, web_functions

###################################################
today = date.today()
# YYmmdd
d1 = today.strftime("%Y%m%d")

homepage = "https://www.bbc.co.uk/news"
hyperlink_text = "papers"
string = d1 + "-"
# Get current date and time
now = datetime.now()

# Build string for exif datetime format
dt_string = now.strftime("%Y:%m:%d %H:%M:%S")
###################################################

logger.remove()  # disable default loguru logging


def version_msg():
    """Return the version."""
    message = "frontpages v%(version)s"
    return message


@click.command()
@click.version_option(__version__, "-V", "--version", message=version_msg())
@click.option(
    "-v", "--verbose", is_flag=True, help="Print debug information", default=False
)
def main(verbose):
    """
    Frontpages will download, convert, apply exif data and rename English
    newspaper front page image files from the BBC News website.
    """

    if verbose is True:
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.add(sys.stderr, level="CRITICAL")

    save_location = Path.home() / "newspaper" / "front-pages"
    Path.mkdir(save_location, parents=True, exist_ok=True)

    list1 = file_functions.files_list(save_location)

    try:
        if file_functions.check_filename(list1, string):
            raise ValueError("Today's image downloads completed previously.")

    except ValueError as e:
        logger.critical(e)
        sys.exit(1)

    newlink = web_functions.find_href(homepage, hyperlink_text)

    fulllink = homepage[:21] + newlink
    logger.info(f"Found weblink: {fulllink}")

    img_list1 = web_functions.get_images(fulllink)

    match_list1 = file_functions.match(img_list1)

    try:
        if not len(match_list1) > 4:
            raise ValueError("No images found, exiting.")

    except ValueError as e:
        logger.critical(e)
        sys.exit(1)

    newtmp = file_functions.create_tmp()

    web_functions.download2(match_list1, newtmp)

    renamelist = file_functions.files_list(newtmp)

    file_functions.rename_all2(renamelist)

    renamelist2 = file_functions.files_list(newtmp)

    file_functions.prepend_date(renamelist2)

    image_functions.pngConvert(newtmp)

    image_functions.jpgDatetime(newtmp, dt_string)

    file_functions.move_files(newtmp, save_location, "jpg")

    file_functions.delete_tmp(newtmp)


if __name__ == "__main__":
    main()

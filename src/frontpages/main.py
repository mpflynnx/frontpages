from datetime import date, datetime
from pathlib import Path

import click

from frontpages import (__version__, file_functions, image_functions,
                        web_functions)

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


def version_msg():
    """Return the version."""
    message = "frontpages v%(version)s"
    return message


@click.command()
@click.version_option(__version__, "-V", "--version", message=version_msg())
def main():
    """
    Frontpages will download, convert, apply exif data and rename English
    newspaper front page image files from the BBC News website.
    """

    save_location = Path.home() / "newspaper" / "front-pages"
    Path.mkdir(save_location, parents=True, exist_ok=True)

    list1 = file_functions.files_list(save_location)

    try:
        if file_functions.check_filename(list1, string):
            raise ValueError(
                f"Filenames starting with '{string}' already exist, exiting."
            )

    except ValueError as e:
        exit(str(e))

    newlink = web_functions.find_href(homepage, hyperlink_text)

    fulllink = homepage[:21] + newlink
    print(fulllink)

    img_list1 = web_functions.get_images(fulllink)

    match_list1 = file_functions.match(img_list1)

    if not len(match_list1) > 4:
        raise ValueError("No images found, exiting.")

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

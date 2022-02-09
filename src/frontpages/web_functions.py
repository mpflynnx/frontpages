import re
import sys
from os.path import basename
from pathlib import Path

import bs4
import requests
from loguru import logger


def find_href(regurl, searchterm):
    """
    Find the href within 'regurl' containing the 'searchterm'.
    """

    lnk = ""
    res = requests.get(regurl)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content, "html.parser")

    for link in soup.find_all(href=re.compile(searchterm), limit=1):
        lnk = link.get("href")

    try:
        if lnk == "":
            raise ValueError(
                f"Couldn't find the search term '{searchterm}' at '{regurl}'"
            )
    except ValueError as e:
        logger.critical(e)
        sys.exit(1)

    return lnk


def get_images(url):
    """
    Get url for images files.
    """
    src = []
    count = 0
    res = requests.get(url)
    res.raise_for_status()
    #  res = htmlFile.read()
    soup = bs4.BeautifulSoup(res.content, "html.parser")
    images = soup.find_all("img", src=True)
    for img in images:
        count += 1
        src.append(img.get("src"))
    logger.info("Found " + str(count) + " images.")
    return src


def download2(mylist, dest):
    """
    Download the url in 'mylist'.
    dest is path-like object.
    """

    downloadcount = 0

    for i in range(len(mylist)):
        downloadcount += 1
        filename = Path(dest / basename(mylist[i]))
        with filename.open(mode="wb") as f:
            f.write(requests.get(mylist[i]).content)

    logger.info("Downloaded " + str(downloadcount) + " images.")

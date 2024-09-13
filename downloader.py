import requests
from bs4 import BeautifulSoup
import os
import threading

url = "https://w47.readnanomachine.com/nano-machine-chapter-?-v5/"
url = var if (var := input("url: ")) != "" else url
filename = "nano-machine"

def grabHref(html: str) -> str:
    if "facebook" in html:
        return ""
    split = html.split('src="')[1]
    return split.split('"')[0]

def downloadImage(url: str, page: int, chapter: int):
    print(chapter, page)
    if not os.path.exists(os.path.join("downloads", filename)):
        os.mkdir(os.path.join("downloads", filename))
    if not os.path.exists(os.path.join("downloads", filename, "chapter-" + str(chapter))):
        os.mkdir(os.path.join("downloads", filename, "chapter-" + str(chapter)))
    response = requests.get(url)

    # test if the picture is the same as any in the ad detection folder
    # if so, don't download it
    for ad in os.listdir("ad-detection"):
        if response.content == open(os.path.join("ad-detection", ad), "rb").read():
            print("ad detected, skipping")
            return

    with open(os.path.join("downloads", filename, "chapter-" + str(chapter), filename + "-" + str(page) + ".jpg"), "wb") as f:
        f.write(response.content)

def get_manga(chapter: int, dropEveryOther: bool = False):
    response = requests.get(url.replace("?", str(chapter)))
    soup = BeautifulSoup(response.text, "html.parser")
    image_set = soup.find_all("img")

    page = 0
    for i in image_set:
        image = ""

        # a = i.contents[0]
        image = grabHref(str(i))
        
        if image != "":
            page += 1
            if dropEveryOther and page % 2 == 0:
                continue
            downloadImage(image, page, chapter)

# 30 - 115, 
get_manga(167, True)
# for i in range(166, 174):
#     try:
#         get_manga(i, True)
#     except Exception as e:
#         print(e)

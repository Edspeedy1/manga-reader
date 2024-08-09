import requests
from bs4 import BeautifulSoup
import os
import threading

url = "https://leviathan-manga.online/manga/leviathan-chapter-?/"
filename = "laviathan"

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
    with open(os.path.join("downloads", filename, "chapter-" + str(chapter), filename + "-" + str(page) + ".jpg"), "wb") as f:
        f.write(response.content)

def get_manga(chapter: int):
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
            downloadImage(image, page, chapter)

# 30 - 115, 
# get_manga(70)
for i in range(75, 215):
    get_manga(i)
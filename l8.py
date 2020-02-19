
import requests
from bs4 import BeautifulSoup
import re
import os

image_dir = "Images"



rootUrl = "http://av.avlang4.co/"

pattern = "read-htm-tid-\d+.html"

img_src = []

def get_detail_page_url(index):

    list_page_url = "%sthread-htm-fid-9-page-%d.html" % (rootUrl,index)

    print("retrieve",list_page_url)

    resp = requests.get(list_page_url)

    if resp.status_code == 200:

        resp.encoding = "GBK"

        soup = BeautifulSoup(resp.text,"html.parser")

        for a in soup.find_all("a"):

            if a.has_attr("href") and a.text != "" :

                detail_url = a.get("href")

                if not not re.match(pattern,detail_url) and len(a.text) >= 3:

                    print(a.text,detail_url)

                    get_image_urls(a.text,detail_url)

def get_image_urls(name,detailurl):

    detailurl = "%s%s" % (rootUrl,detailurl)

    resp = requests.get(detailurl)

    if resp.status_code == 200:

        resp.encoding = "GBK"

        soup = BeautifulSoup(resp.text,"html.parser")

        i = 1

        for img in soup.find_all("img"):

            if img.has_attr("src"):

                src = img.get("src")

                if src.startswith("http") and src.endswith("jpg"):

                    if not src in img_src:

                        img_src.append(src)

                        #downlaod image

                        try:

                            resp = requests.get(src,timeout=5)

                            if resp.status_code == 200:

                                image_name = "%s-%d.jpg" % (name,i)

                                with open(os.path.join(image_dir,image_name),"wb") as f:
                                    f.write(resp.content)

                                print( "已下载" , image_name,src)

                                i = i+1
                        except:
                            print("下载失败",src)


def main():

    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    for i in range(1,200):
        get_detail_page_url(i)


if __name__ == "__main__":
    main()


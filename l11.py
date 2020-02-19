import requests_async
import re
from bs4 import BeautifulSoup
import os

img_dir = "images"

rootUrl = "http://av.avlang4.co/"

img_srcs = []


#     list_page_url = "%sthread-htm-fid-9-page-%d.html" % (rootUrl,index)

async def _get_detail_page_url(index):
    list_page_url = f"{rootUrl}thread-htm-fid-5-page-{index}.html"

    resp = await requests_async.get(list_page_url)

    if resp.status_code == 200:

        resp.encoding = "GBK"

        soup = BeautifulSoup(resp.text, "html.parser")

        def _filter(a):
            if a.has_attr("href"):

                return not a.find("b") and re.search(r"^read-htm-tid-\d+(-page-\d+)?.html$",
                                                     a.get("href")) and re.search(r"[a-zA-Z\u4E00-\u9FA5\s]+", a.text)
            else:
                return False

        tasks = [_get_image_url(index, a.get("href")) for a in filter(_filter, soup.find_all("a"))]

        await asyncio.gather(*tasks)


async def _get_image_url(index, detailurl):
    detailurl = f"{rootUrl}{detailurl}"

    resp = await requests_async.get(detailurl)

    if resp.status_code == 200:

        resp.encoding = "GBK"

        soup = BeautifulSoup(resp.text, "html.parser")

        def _filter(img):
            if img.has_attr("src"):
                src = img.get("src")
                if src.startswith("http") and src.endswith("jpg") and src not in img_srcs:
                    return True
                else:
                    img_srcs.append(src)
                    return False

        tasks = [_download_img(f"{soup.text}-{index + 1}.jpg", img.get("src")) for (index, img) in
                 enumerate(filter(_filter, soup.find_all("img")))]

        await asyncio.gather(*tasks)


async def _download_img(img_name, src):
    try:
        resp = await requests_async.get(src)

        with open(os.path.join(img_dir, img_name)) as f:
            f.write(resp.content)
            print("Success", img_name, src)
    except:
        print("Failue")


# 15864020255

async def main():
    await _get_detail_page_url(1)


if __name__ == "__main__":

    import asyncio

    if not os.path.isdir(img_dir):
        os.mkdir(img_dir)

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())
    except:
        loop.close()

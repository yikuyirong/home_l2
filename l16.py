
import requests
from bs4 import BeautifulSoup
import asyncio
import os


url = "https://mp.weixin.qq.com/s?srcid=&scene=23&sharer_sharetime=1580188309519&mid=2247491953&sharer_shareid=dc66b101b997fea5e9aad2afce1806b6&sn=d4ad82cd8e24df3ba87ae22b58c484c3&idx=3&__biz=MzI0MjQ3ODkyOQ%3D%3D&chksm=e9791b4fde0e92592ae4faa8139a98b6ac4f2521e18e618ed6b504d6f5a635ecd138eee6d129&mpshare=1#rd"


download_dir = "三年级语文下册"


async def fetch_imgs():

    resp = requests.get(url)

    if resp.status_code == 200:

        soup = BeautifulSoup(resp.text,"html.parser")

        # <img class="rich_pages " data-ratio="1.413888888888889" data-s="300,640" data-src="https://mmbiz.qpic.cn/mmbiz_jpg/PgvhUtx3ibcgr57JyP5ZJtHG17fDV3dPtadYmkAdcWiblP23wAiaaPcfu7GmTmRyrSXkEicVmicERR1KicKzicOlMd8oQ/640?wx_fmt=jpeg" data-type="jpeg" data-w="1080" style="width: 677px !important; height: auto !important; visibility: visible !important;" _width="677px" src="https://mmbiz.qpic.cn/mmbiz_jpg/PgvhUtx3ibcgr57JyP5ZJtHG17fDV3dPtadYmkAdcWiblP23wAiaaPcfu7GmTmRyrSXkEicVmicERR1KicKzicOlMd8oQ/640?wx_fmt=jpeg&amp;tp=webp&amp;wxfrom=5&amp;wx_lazy=1&amp;wx_co=1" crossorigin="anonymous" data-fail="0">

        # print(resp.text)

        srcs = []

        for img in soup.find_all("img"):

            if img.has_attr("data-src"):

                srcs.append(img.get("data-src"))


        await asyncio.gather(*[ download_img(index,src) for (index,src) in enumerate(srcs)])

    else:

        raise Exception(f"{resp.status_code} {resp.raise_for_status()}")


async def download_img(index,url):

    print("开始下载",index,url)

    resp = requests.get(url)

    if resp.status_code == 200:

        if not os.path.isdir(download_dir):
            os.mkdir(download_dir)

        with open(os.path.join(download_dir,"%03d.webp" % index),"wb") as f:
            f.write(resp.content)
        print("下载成功",index,url)
    else:
        raise Exception(f"{resp.status_code} {resp.raise_for_status()}")


async def main():

    await fetch_imgs()




if __name__ == "__main__":

    asyncio.get_event_loop().run_until_complete(main())




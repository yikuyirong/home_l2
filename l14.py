import asyncio
import requests_async
import requests
import re
from bs4 import BeautifulSoup
import json
import os

root_url = "http://db.jndjg.cn/"

download_dir = "lessons"


async def fetch_grade():
    url = f"{root_url}index.aspx?menutype=84&subtype=95"

    resp = await requests_async.get(url)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "html.parser")

        nav = soup.find("nav", attrs={"id": "third_box"})

        if nav:

            tasks = []

            for a in nav.find_all("a"):
                title = a.text

                url = a.get("href")

                (type_id, tow_id, third_id) = re.findall(r"\d+", url)

                # print(title,type_id,tow_id,third_id)

                # await fetch_type(title,type_id,tow_id,third_id)

                tasks.append(fetch_type(title, type_id, tow_id, third_id))

            # await asyncio.gather(*tasks)

            for task in tasks:
                await  task


async def fetch_type(title, type_id, tow_id, third_id):
    url = f"{root_url}GetInfoList.ashx?type={type_id}&towid={tow_id}&thirdid={third_id}&sorttype=recommend&area=0&time=0&num=12"

    resp = await requests_async.get(url)

    if resp.status_code == 200:

        j = json.loads(resp.text)

        dir = os.path.join(download_dir, title)

        if not os.path.isdir(dir):
            os.mkdir(dir)

        dirs = os.listdir(dir)

        tasks = []

        for info in j["infoList"]:

            name = re.sub(r"[\\*/]", "_", info["moviename"])

            if f"{name}.mp4" not in dirs:
                tasks.append(fetch_movie(info["movieid"], title, name))
                print(title, name)

        # await asyncio.gather(*tasks)

        for task in tasks:
            await  task


async def fetch_movie(movie_id, title, movie_name):
    url = f"{root_url}video.aspx?id={movie_id}"

    resp = await requests_async.get(url)

    if resp.status_code == 200:

        soup = BeautifulSoup(resp.text, "html.parser")

        video = soup.find("source")

        if video:
            # print(title,movie_name,video.get("src"))
            await download_movie(title, movie_name, video.get("src"))


async def download_movie(title, name, url):
    try:

        print("开始下载", title, name, url)
        # resp = await requests_async.get(url)
        resp = requests.get(url, stream=True)

        if resp.status_code == 200:

            dir = os.path.join(download_dir, title)

            total = float(resp.headers["content-length"])

            size = 0

            with open(os.path.join(dir, f"{name}.mp4"), "ab") as f:

                # f.write(resp.content)

                for chunk in resp.iter_content(chunk_size=2048):
                    if chunk:
                        size = size + len(chunk)
                        f.write(chunk)

                        print("\r%.2f%%" % (size * 100 / total), end="")

    except Exception as e:
        print("\033[1;31m下载失败\033[0m", title, name, url, str(e))
    else:
        print("下载成功", title, name, url)


async def main():
    await fetch_grade()


if __name__ == "__main__":

    if not os.path.isdir(download_dir):
        os.mkdir(download_dir)

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())
    except Exception as e:
        print(e)
        if loop.is_running():
            loop.close()

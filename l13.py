import asyncio
import urllib.parse
import requests
import requests_async
import re
from bs4 import BeautifulSoup

results = []


async def get_shici(keyword, index=1):
    url = f"https://so.gushiwen.org/search.aspx?page={index}&value={urllib.parse.quote(keyword)}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }

    resp = requests.get(url, headers=headers)

    resp.close()

    if resp.status_code == 200:

        soup = BeautifulSoup(resp.text, "html.parser")

        for cont in soup.find_all(name="div", attrs="cont"):

            # print(cont)

            title = cont.find(name="p", attrs="")

            if title:
                author = cont.find("p", attrs={"class": "source"})

                contson = cont.find_all(name="div", attrs="contson")

                if author and contson and len(contson) > 0:

                    title = re.sub('\s+', '', title.text) #题目

                    author = re.sub('\s+', '', author.text) #作者

                    print(f"{index} \033[1;31m{title}\033[0m")

                    print(author)

                    for contson in cont.find_all(name="div", attrs="contson"):
                        print(re.sub("\s+", "", contson.text))

        if index < 10:
            await get_shici(keyword, index + 1)
    else:
        print(resp.status_code)


async def main():
    while True:

        keywords = input("\033[1m请输入你想检索的诗人或作品名：\033[0m")

        if keywords.lower() in ["q", "e", "quit", "exit"]:
            break

        if keywords == "":
            keywords = "张养浩"

        for keyword in re.split(r"\s+", keywords):
            await get_shici(keyword)


if __name__ == "__main__":

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())
    except BaseException as e:

        print("Error", str(e))

        if loop.is_running():
            loop.close()

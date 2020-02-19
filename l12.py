
import asyncio
import requests_async
from bs4 import BeautifulSoup

class Program(object):

    url = "https://pic.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=&st=-1&fm=result&fr=&sf=1&fmq=1580990415450_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&sid=&word=%s"



    async def search(self, keyword,retry = 5):

        try:
            url = self.url % keyword

            resp = await requests_async.get(url)

            await resp.close()

            soup = BeautifulSoup(resp.text,"html.parser")

            for (index,img) in enumerate(soup.find_all("img")):
                print(index,img)



        except:
            if retry > 0:
                await self.search(keyword,retry - 1)

if __name__ == "__main__":

    p =  Program()

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(p.search("美女"))
    except:
        loop.close()









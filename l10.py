
import re

hrefs = ["http://www.aaa.com/read-htm-tid-123.html","http://www.aaa.com/read-htm-tid-123-fpage-1.html"]

pattern = r"read-htm-tid-\d+(-fpage-\d+)?"

for href in hrefs:
    result = re.search(pattern,href)
    print(not not result)
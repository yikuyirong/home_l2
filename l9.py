
import re

reg = "read-htm-tid-\d+.html"
str = "read-htm-tid-123333.123.html"

result = re.match(reg,str)

print(not not result)
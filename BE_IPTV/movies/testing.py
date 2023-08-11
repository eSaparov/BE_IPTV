from urllib import error
from urllib.request import urlopen
import urllib.request
import os
import json


url = "https://gist.githubusercontent.com/nextsux/f6e0327857c88caedd2dab13affb72c1/raw/04441487d90a0a05831835413f5942d58026d321/videos.json"

response = urlopen(url)
data_json = json.loads(response.read())

# for data in data_json:
#     photoUrl = data['iconUri']
#     photoname = 'C:/Users/SUMBAR/Desktop/seznam/BE_IPTV/static/images/'+photoUrl.rsplit('/', 1)[-1]
#     print(photoUrl.rsplit('/', 1)[-1])
    
#     try:
#         urllib.request.urlretrieve(photoUrl, photoname)
#     except error.URLError as e:
#         print(e.reason)

photoname = os.path.abspath(os.curdir)
print(photoname)

# piclist = os.listdir(photoname)
# if not "azure.png" in piclist:
#     print("pizdec")
# print("hrenase")

# from PIL import Image

# img = Image.open(photoname)
# img.show()
import requests
from pprint import pprint
from json import JSONDecoder, JSONEncoder

file_num = 3
file = open('original{}.pdf'.format(file_num), 'rb')
url = 'http://127.0.0.1:5000/upload'
decoder = JSONDecoder()

req = requests.post(url=url, files={'pdf_input': file})
data = decoder.decode(req.text)
pprint(data)

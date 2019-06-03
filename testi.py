import os
from bs4 import BeautifulSoup as BS
from base64 import b64decode


path = '/home/h/dump/gaussian_process.html'
with open(path, 'rb') as rf:
    content = rf.read()
    soup = BS(content, 'html.parser')
    images = soup.find_all('img')

path2 = '/mnt/c/users/hp/Desktop/'
for i, data_uri in enumerate(images):
    image_name = 'image' + str(i) + '.png'
    image_path = os.path.join(path2, image_name)
    data_uri = "data:image/png;base64,iVBORw0KGg..."
    header, encoded = data_uri.split(",", 1)
    data = b64decode(encoded)
    with open(image_path, 'wb') as wf:
        wf.write(data)


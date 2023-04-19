import os
import requests
from bs4 import BeautifulSoup

url = 'https://www.gsmarena.com/samsung_galaxy_s20+-pictures-10080.php'
folder = 'samsung-s2oplus'
path = f'/home/emma/Downloads/gsmarena-imgs/{folder}/'

# scrape entry
image_container_div_id = 'binkies-container' #'pictures-list'


def fetchBody():
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return response.raise_for_status()


def parseBody(body):
    soup = BeautifulSoup(body, 'html.parser')
    pics_container = soup.body.find(id=image_container_div_id)
    img_tags = pics_container.find_next_siblings('img')

    imgs_links = []
    for tag in img_tags:
        print(tag)
        data_src = tag.attrs.get('data-src')
        src = tag.attrs.get('src')
        if tag.name == 'img' and data_src != None:
            imgs_links.append(data_src)
        if tag.name == 'img' and src != None:
            imgs_links.append(src)

    if (len(imgs_links) < 0):
        raise Exception('no image links found')

    return imgs_links


def downloadImage(img):
    imgRaw = requests.get(img).content
    imgName = img.split('/')[-1]
    print('saving >> ', imgName)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+imgName, 'wb') as writer:
        writer.write(imgRaw)


if __name__ == '__main__':
    try:
        body = fetchBody();
        imgs_links = parseBody(body)
        # save
        for link in imgs_links:
            downloadImage(link)
    except:
        print('failed. shouldn\'t happen')



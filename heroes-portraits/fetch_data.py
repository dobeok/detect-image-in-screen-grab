import requests
import time
import random
from bs4 import BeautifulSoup


if __name__ == '__main__':
    url = 'https://dota2.fandom.com/wiki/Category:Hero_icons'
    r = requests.get(url)
    r.status_code


    soup = BeautifulSoup(r.text, 'html.parser')

    gallery = soup.find_all('li', attrs={'class': 'gallerybox'})
    len(gallery)
    gallery[0].find_all('a')


    for gallery_item in gallery:
        data = gallery_item.find_all('a', attrs={'class': 'image'})[0]
        hero_name = data.find_all('img')[0]['alt']
        image_link = data['href']
        print(hero_name, image_link)

        img_data = requests.get(image_link)
        if img_data.status_code == 200:
            img_data = img_data.content
            with open(f'./images/{hero_name}', 'wb') as handler:
                handler.write(img_data)
        time.sleep(random.random() * 3)
import requests
import json
import os
from tqdm import tqdm
# import spliter

image_path = 'cross.png'


def download_img():
    folder = './results/Midjourney/images'
    file_path = './results/Midjourney/prompt_img_pair.json'
    with open(file_path, 'r') as f:
        prompt_img_pairs = json.load(f)
    
    i = 0
    cross_imgs = []
    for url in list(prompt_img_pairs.values()):
        if url == 'fail':
            with open(image_path, 'rb') as image_file:
                img_data = image_file.read()
                cross_imgs.append(i)
        else:
            img_data = requests.get(url).content
        img_path = folder+'/{}.jpg'.format(i)
        i += 1
        with open(img_path, 'wb') as handler:
            handler.write(img_data)

    with open('./results/Midjourney/cross_idx', 'w') as f:
        json.dump(cross_imgs, f, indent=4)
    
if __name__ == '__main__':
    download_img()
    print('Done!')
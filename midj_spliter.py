import subprocess
from PIL import Image
import json
import os
import shutil

def split():
    file_path = './results/Midjourney/images'
    with open('./results/Midjourney/cross_idx', 'r') as f:
        cross_idx = json.load(f)

    for path in os.listdir(file_path):
        if path == '.DS_Store':
            continue
        idx = int(path.split('.')[0])
        img_path = file_path + '/' + path
        if idx in cross_idx:
            #duplicate cross 4 times
            for i in range(4):
                new_path = file_path + '/' + str(idx) + '_' + str(i) + '.jpg'
                shutil.copy(img_path, new_path)
            bash_command_remove = 'rm {}'.format(img_path)
            subprocess.run(bash_command_remove, shell=True, capture_output=True, text=True)
            continue
        
        bash_command_split = 'split-image ' + img_path + ' 2 2 --output-dir ' + file_path
        bash_command_remove = 'rm {}'.format(img_path)

        subprocess.run(bash_command_split, shell=True, capture_output=True, text=True)
        subprocess.run(bash_command_remove, shell=True, capture_output=True, text=True)

def resize():
    file_path = './results/Midjourney/images'
    for path in os.listdir(file_path):
        if path == '.DS_Store':
            continue
        img_path = file_path + '/' + path
        img = Image.open(img_path)
        # img = img.resize((256, 256))
        # img.save(img_path)
        size = img.size
        img = img.resize((int(size[0]*2), int(size[1]*2)))
        img = img.convert('RGB')
        img.save(img_path)


if __name__ == '__main__':
    split()
    resize()
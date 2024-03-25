import requests
import json
import os
from tqdm import tqdm
import midj_generator as mg

def get_prompts():
    with open('./files/prompts.json', 'r') as f:
        prompts = json.load(f)
    return prompts


def compensate_img():
    with open('./files/midj_miss_index.json', 'r') as f:
        idx = json.load(f)
    prompts = get_prompts()
    for i in idx:
        selected_prompt = prompts[str(i)]
        mg.generate(selected_prompt)
    

if __name__ == '__main__':
    compensate_img()
    print('Done!')
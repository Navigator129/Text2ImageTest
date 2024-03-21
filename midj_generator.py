import requests
import json
import time
import random
from discord.ext import commands
import midj_crawler as cr
import midj_download as md
import midj_spliter as ms


def prepare_prompt():
    with open('./files/prompts.json', 'r') as f:
        prompts = json.load(f)
    prompt_list = list(prompts.values())
    return prompt_list

def generate():
    url = 'https://discord.com/api/v9/interactions'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        "authorization": "NDgwNTkyNzQ1NzMyNTA1NjAw.GNLO5A.sAh1CUG_D3PCidJfEJl2PpJPpuMvzo2ZoZXIJA",
        "Referer": "https://discord.com/channels/1093795199546826812/1220419144558837790",
    }

    prompt_list = prepare_prompt()
    i = 0
    for prompt in prompt_list:
        nonce = str(random.randint(10 ** 10, 10 ** 19 - 1))
        payload = {"type":2,"application_id":"936929561302675456","guild_id":"1093795199546826812","channel_id":"1220419144558837790","session_id":"c14cc9c1219654391ae09bd9e3d98398","data":{"version":"1166847114203123795","id":"938956540159881230","name":"imagine","type":1,"options":[{"type":3,"name":"prompt","value":prompt}],"application_command":{"id":"938956540159881230","type":1,"application_id":"936929561302675456","version":"1166847114203123795","name":"imagine","description":"Create images with Midjourney","options":[{"type":3,"name":"prompt","description":"The prompt to imagine","required":True,"description_localized":"The prompt to imagine","name_localized":"prompt"}],"integration_types":[0],"global_popularity_rank":1,"description_localized":"Create images with Midjourney","name_localized":"imagine"},"attachments":[]},"nonce":nonce,"analytics_location":"slash_ui"}


        response = requests.post(url, headers=headers, json = payload)
        print(response.status_code)
        time.sleep(15)
        i += 1
        if i%50 == 0:
            cr.crawler()
            md.download_img()
    #收尾
    cr.crawler()
    md.download_img()
    ms.split()
    ms.resize()
    print('Done!')


if __name__ == '__main__':
    generate()
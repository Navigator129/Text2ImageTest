import requests
import json
import time
import random


def fetch_prompt(path):
    prompts = []
    with open(path, 'r') as f:
        dict_ = json.load(f)
    for prompt_dict in dict_:
        prompts.append(prompt_dict['prompt'])
    return prompts

def generate(input_prompt, channel_id):
    url = 'https://discord.com/api/v9/interactions'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        "authorization": "NDgwNTkyNzQ1NzMyNTA1NjAw.Gf5L4x.Ad2Jr8T8Uolevo83O3Eakp8Ooa7HB_n5ECCuCU",
        "Referer": "https://discord.com/channels/1093795199546826812/{}".format(channel_id),
    }

    prompt = input_prompt
    nonce = str(random.randint(10 ** 10, 10 ** 19 - 1))
    payload = {"type":2,"application_id":"936929561302675456","guild_id":"1093795199546826812","channel_id":"{}".format(channel_id),"session_id":"59633cdff1e72294a2358a5031e88484","data":{"version":"1237876415471554623","id":"938956540159881230","name":"imagine","type":1,"options":[{"type":3,"name":"prompt","value":prompt}],"application_command":{"id":"938956540159881230","type":1,"application_id":"936929561302675456","version":"1237876415471554623","name":"imagine","description":"Create images with Midjourney","options":[{"type":3,"name":"prompt","description":"The prompt to imagine","required":True,"description_localized":"The prompt to imagine","name_localized":"prompt"}],"dm_permission":True,"contexts":[0,1,2],"integration_types":[0,1],"global_popularity_rank":1,"description_localized":"Create images with Midjourney","name_localized":"imagine"},"attachments":[]},"nonce":nonce,"analytics_location":"slash_ui"}


    response = requests.post(url, headers=headers, json = payload)
    print(response.status_code)
    time.sleep(7)
    #收尾
    print('Done!')


def compensate(input_prompt, channel_id):
    url = 'https://discord.com/api/v9/interactions'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        "authorization": "NDgwNTkyNzQ1NzMyNTA1NjAw.GNLO5A.sAh1CUG_D3PCidJfEJl2PpJPpuMvzo2ZoZXIJA",
        "Referer": "https://discord.com/channels/1093795199546826812/{}".format(channel_id),
    }

    prompt = input_prompt
    nonce = str(random.randint(10 ** 10, 10 ** 19 - 1))
    payload = {"type":2,"application_id":"936929561302675456","guild_id":"1093795199546826812","channel_id":"{}".format(channel_id),"session_id":"c14cc9c1219654391ae09bd9e3d98398","data":{"version":"1166847114203123795","id":"938956540159881230","name":"imagine","type":1,"options":[{"type":3,"name":"prompt","value":prompt}],"application_command":{"id":"938956540159881230","type":1,"application_id":"936929561302675456","version":"1166847114203123795","name":"imagine","description":"Create images with Midjourney","options":[{"type":3,"name":"prompt","description":"The prompt to imagine","required":True,"description_localized":"The prompt to imagine","name_localized":"prompt"}],"integration_types":[0],"global_popularity_rank":1,"description_localized":"Create images with Midjourney","name_localized":"imagine"},"attachments":[]},"nonce":nonce,"analytics_location":"slash_ui"}


    response = requests.post(url, headers=headers, json = payload)
    print(response.status_code)
    time.sleep(5)
    #收尾
    print('Done!')


if __name__ == '__main__':
    relate_seed_path = './files/exp2/related_seed_prompts.json'
    unrelated_seed_path = './files/exp2/unrelated_seed_prompts.json'
    related_mutate_path = './files/exp2/related_mutate_prompts.json'
    unrelated_mutate_path = './files/exp2/unrelated_mutate_prompts.json'
    related_prompts = fetch_prompt(relate_seed_path) + fetch_prompt(related_mutate_path)
    unrelated_prompts = fetch_prompt(unrelated_seed_path) + fetch_prompt(unrelated_mutate_path)

    related_channel_id = '1282072651921358899'
    unrelated_channel_id = '1282072689971957864'
    # for prompt in related_prompts:
    #     generate(prompt, related_channel_id)
    for prompt in unrelated_prompts:
        generate(prompt, unrelated_channel_id)

    print('finish')
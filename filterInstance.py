import requests
import time
import random
from tqdm import tqdm


def generate(input_prompt, channel_id):
    url = 'https://discord.com/api/v9/interactions'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        "authorization": "token",
        "Referer": "https://discord.com/channels/1093795199546826812/{}".format(channel_id),
    }

    prompt = input_prompt
    nonce = str(random.randint(10 ** 10, 10 ** 19 - 1))
    payload = {"type":2,"application_id":"936929561302675456","guild_id":"1093795199546826812","channel_id":"{}".format(channel_id),"session_id":"632184cb8a28ace933ab3fde7e7c7277","data":{"version":"1237876415471554623","id":"938956540159881230","name":"imagine","type":1,"options":[{"type":3,"name":"prompt","value":prompt}],"application_command":{"id":"938956540159881230","type":1,"application_id":"936929561302675456","version":"1237876415471554623","name":"imagine","description":"Create images with Midjourney","options":[{"type":3,"name":"prompt","description":"The prompt to imagine","required":True,"description_localized":"The prompt to imagine","name_localized":"prompt"}],"dm_permission":True,"contexts":[0,1,2],"integration_types":[0,1],"global_popularity_rank":1,"description_localized":"Create images with Midjourney","name_localized":"imagine"},"attachments":[]},"nonce":nonce,"analytics_location":"slash_ui"}

    response = requests.post(url, headers=headers, json = payload)
    print(response.status_code)
    time.sleep(7)
    #收尾
    print('Done!')

if __name__ == '__main__':
    channel_id = '1347218877532209216'
    prompts = 'a cat is to the right of a dog'
    for i in tqdm(range(50)):
        generate(prompts, channel_id)
        time.sleep(1)
    print('Done with prompt {}'.format(i))
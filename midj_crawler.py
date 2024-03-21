import json
import os
import requests
import re
from tqdm import tqdm



def save_url(dict_):
    filepath = './results/Midjourney/prompt_img_pair.json'
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            json.dump(dict_, f, indent=4)
    else:
        with open(filepath, 'r') as f:
            prev_dict = json.load(f)
        prev_dict.update(dict_)
        with open(filepath, 'w') as f:
            json.dump(prev_dict, f, indent=4)
       


def crawler():
    img_url = 'https://discord.com/api/v9/channels/1218116993232801854/messages?limit=50'
    header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    "accept": "*/*",
    "accept-language": "en,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7",
    "authorization": "NDgwNTkyNzQ1NzMyNTA1NjAw.GNLO5A.sAh1CUG_D3PCidJfEJl2PpJPpuMvzo2ZoZXIJA",
    "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-debug-options": "bugReporterEnabled",
    "x-discord-locale": "en-US",
    "x-discord-timezone": "Asia/Singapore",
    "x-super-properties": "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IkNocm9tZSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbiIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMTQuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjExNC4wLjAuMCIsIm9zX3ZlcnNpb24iOiIxMC4xNS43IiwicmVmZXJyZXIiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyIsInJlZmVycmluZ19kb21haW4iOiJ3d3cuZ29vZ2xlLmNvbSIsInNlYXJjaF9lbmdpbmUiOiJnb29nbGUiLCJyZWZlcnJlcl9jdXJyZW50IjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiJ3d3cuZ29vZ2xlLmNvbSIsInNlYXJjaF9lbmdpbmVfY3VycmVudCI6Imdvb2dsZSIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjIxMTY0NCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=",
    "cookie": "__dcfduid=0e15c4d01d9e11eeb9b25f4f8eff00cf; __sdcfduid=0e15c4d11d9e11eeb9b25f4f8eff00cf65156fc60b0a8e32c0e63e37a931299f98a770b9179ff9e08dc6b35c1ea34991; __cfruid=afbece693a02dea8d134244fbb3c007049946574-1688827517; locale=en-US; _gcl_au=1.1.1637467285.1688827518; _ga=GA1.1.631576661.1688827519; OptanonConsent=isIABGlobal=false&datestamp=Sat+Jul+08+2023+22%3A45%3A18+GMT%2B0800+(Singapore+Standard+Time)&version=6.33.0&hosts=&landingPath=https%3A%2F%2Fdiscord.com%2F&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1; _ga_Q149DFWHT7=GS1.1.1688827518.1.0.1688827522.0.0.0",
    "Referer": "https://discord.com/channels/1093795199546826812/1093806443829928027",
    "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    response = requests.get(url=img_url, headers=header)
    response_json = response.json()
    for img_data in tqdm(response_json):
        if img_data['attachments']:
            prompt = img_data['content']
            img_url = img_data['attachments'][0]['url']

            pattern = r'\*\*(.*?)\*\*'
            match = re.search(pattern, prompt)
            prompt = match.group(1)
            if 'https://cdn.discordapp.com' not in img_url:
                img_url = 'fail'
            prompt_img_dict = {prompt: img_url}
            save_url(prompt_img_dict)
    

# if __name__ == '__main__':
#     crawler()
#     print('Done!')

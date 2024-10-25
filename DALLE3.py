import json
from openai import OpenAI
from tqdm import tqdm
import os
import openai
import requests

# Replace YOUR_API_KEY with your OpenAI API key
client = OpenAI(api_key = "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")
def fetch_prompt(file_path):
    prompts = []
    with open(file_path, "r") as file:
        data = json.load(file)
    for dict_ in data:
        prompts.append(dict_["prompt"])
    return prompts

def generate(prompts):
    urls = []
    i = 0 
    for p in tqdm(prompts):
        try:
            response = client.images.generate(
            model="dall-e-3",
            prompt = p,
            size="1024x1024",
            quality="standard",
            n=1,
            )
            
            url = response.data[0].url
            dict_ = {'index': i, 'url': url}
            urls.append(dict_)
        except openai.BadRequestError as e:
            print('Error at index:', i)
            continue
        i += 1
    return urls

def save_urls(urls, file_path):
    with open(file_path, "w") as file:
        json.dump(urls, file)
    return file_path

def get_urls(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def download(urls, check):
    if check:
        save_path = "./images/DALLE3/exp3/related/"
    else:
        save_path = "./images/DALLE3/exp3/unrelated/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    for dict_ in urls:
        index = dict_['index']
        url = dict_['url']
        file_path = os.path.join(save_path, "{}.jpg".format(index))
        img_data = requests.get(url).content
        with open(file_path, 'wb') as handler:
            handler.write(img_data)



if __name__ == "__main__":
    file_path1 = './files/exp{}/related_seed_prompts.json'.format(3)
    file_path2 = './files/exp{}/related_mutate_prompts.json'.format(3)
    file_path3 = './files/exp{}/unrelated_seed_prompts.json'.format(3)
    file_path4 = './files/exp{}/unrelated_mutate_prompts.json'.format(3)
    prompt_list1 = fetch_prompt(file_path1)
    prompt_list2 = fetch_prompt(file_path2)
    prompt_list3 = fetch_prompt(file_path3)
    prompt_list4 = fetch_prompt(file_path4)
    
    related_prompts = prompt_list1 + prompt_list2
    unrelated_prompts = prompt_list3 + prompt_list4

    related_urls = generate(related_prompts)
    unrelated_urls = generate(unrelated_prompts)
    save_urls(related_urls, './images/DALLE3/exp3/related_urls.json')
    save_urls(unrelated_urls, './images/DALLE3/exp3/unrelated_urls.json')
    related_urls = get_urls('./images/DALLE3/exp3/related_urls.json')
    unrelated_urls = get_urls('./images/DALLE3/exp3/unrelated_urls.json')
    download(related_urls, True)
    download(unrelated_urls, False)
    


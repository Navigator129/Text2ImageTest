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

def generate(prompts, check):
    total_prompts = len(prompts)
    for i in tqdm(range(150, total_prompts)):
        try:
            p = total_prompts[i]
            response = client.images.generate(
            model="dall-e-3",
            prompt = p,
            size="1024x1024",
            quality="standard",
            n=1,
            )
            
            url = response.data[0].url
            download(url, check, i)
        except openai.BadRequestError as e:
            print('Error at index:', i)
            continue

# def save_urls(urls, file_path):
#     with open(file_path, "w") as file:
#         json.dump(urls, file)
#     return file_path

# def get_urls(file_path):
#     with open(file_path, "r") as file:
#         data = json.load(file)
#     return data

def download(url, check, index):
    if check:
        save_path = "./images/DALLE3/exp1/related/"
    else:
        save_path = "./images/DALLE3/exp1/unrelated/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # for dict_ in urls:
    #     index = dict_['index']
    #     url = dict_['url']
    file_path = os.path.join(save_path, "{}.jpg".format(index))
    img_data = requests.get(url)
    if img_data.status_code == 200:
        with open(file_path, 'wb') as handler:
            handler.write(img_data.content)
    else:
        print('Error at index:', index)

if __name__ == "__main__":
    file_path1 = './files/exp{}/related_seed_prompts.json'.format(1)
    file_path2 = './files/exp{}/related_mutate_prompts.json'.format(1)
    file_path3 = './files/exp{}/unrelated_seed_prompts.json'.format(1)
    file_path4 = './files/exp{}/unrelated_mutate_prompts.json'.format(1)
    prompt_list1 = fetch_prompt(file_path1)
    prompt_list2 = fetch_prompt(file_path2)
    prompt_list3 = fetch_prompt(file_path3)
    prompt_list4 = fetch_prompt(file_path4)
    
    related_prompts = prompt_list1 + prompt_list2
    unrelated_prompts = prompt_list3 + prompt_list4

    related_urls = generate(related_prompts, True)
    unrelated_urls = generate(unrelated_prompts, False)
    


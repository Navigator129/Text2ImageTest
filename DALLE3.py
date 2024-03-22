import json
from openai import OpenAI
from tqdm import tqdm
import os
import openai
import requests

# Replace YOUR_API_KEY with your OpenAI API key
client = OpenAI(api_key = "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")

def fetch_prompt():
    with open("./files/prompts.json", "r") as f:
        return json.load(f)

def generate():
    prompt_list = fetch_prompt()
    urls = []
    for i in tqdm(range(127, len(prompt_list))):
        try:
            response = client.images.generate(
            model="dall-e-3",
            prompt = prompt_list[str(i)],
            size="1024x1024",
            quality="standard",
            n=1,
            )
            
            url = response.data[0].url
            urls.append(url)
        except openai.BadRequestError as e:
            print(i)
            continue
    with open("./results/DALLE3/dall_url.json", "w") as f:
        json.dump(urls, f)

def download():
    with open("./results/DALLE3/dall_url.json", "r") as file:
        urls = json.load(file)
    i = 0
    for url in urls:
        file_path = os.path.join("./results/DALLE3/images", "test_case_{}.png".format(i))
        img_data = requests.get(url).content
        with open(file_path, 'wb') as handler:
            handler.write(img_data)
        i += 1
if __name__ == "__main__":
    generate()
    # download()
    


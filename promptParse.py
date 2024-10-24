import json
import os
from openai import OpenAI
from mutatePPT import *
from constructPPT import *
from tqdm import tqdm


gpt_value = {"key": "sk-proj-1BPvHk5XzjyLbAc1UPy5T3BlbkFJSuwD9Ey30jzLFHcL30ZD",
            "org": "YOUR_ORG_ID",}


def get_prompt_list(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    prompt_list = []
    for item in data:
        prompt_list.append(item['prompt'].strip())
    return prompt_list

def promptParse(prompt):
    final_result = []
    client = OpenAI(api_key=gpt_value['key'])
    user_msg = """
            You are an expert in parsing prompt into a tree structure. I will give you a simple prompt and you need to return me the data structure as below example:
            
            "prompt": "One foldable green dining table is underneath one torn blue book."
            "PPT": {
                        "relation": "Underneath",
                        "obj1": "dining table",
                        "obj1_attr": [
                            "Foldable",
                            "green",
                            "one"
                        ],
                        "obj2": "book",
                        "obj2_attr": [
                            "Torn",
                            "blue",
                            "one"
                        ]
                    }
            

            Now is the given prompt:
            
        """ + prompt
    response = client.chat.completions.create(
        model = "gpt-4",
        messages=[
        {"role": "user", "content": user_msg}]
    )
    structure = response.choices[0].message.content
    data = json.loads(structure)
    final_result.append(data)
    return final_result

if __name__ == '__main__':
    file_path = './files/test/related_seed_prompts.json'
    prompt_list = get_prompt_list(file_path)
    final_result = []
    for prompt in tqdm(prompt_list):
        result = promptParse(prompt)
        final_result.append(result)
    print(final_result)
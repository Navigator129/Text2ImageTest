import json
from openai import OpenAI
import os

gpt_value = {"key": "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",
            "org": "org-YGi1QDMf6n1Ptr1pxMZHsYpE"}


def get_error_results(path):
    with open(path, 'r') as f:
        results = json.load(f)
    return results

def get_PPTs(path):
    with open(path, 'r') as f:
        PPTs = json.load(f)
    return PPTs

def get_results():
    v10_path = './results/Stable_Diffusion/v1-5/result.json'
    v15_path = './results/Stable_Diffusion/v1-5/result.json'
    v21_path = './results/Stable_Diffusion/v1-5/result.json'
    midj_path = './results/Stable_Diffusion/v1-5/result.json'
    dalle_path = './results/Stable_Diffusion/v1-5/result.json'

    v10_results = get_error_results(v10_path)
    v15_results = get_error_results(v15_path)
    v21_results = get_error_results(v21_path)
    midj_results = get_error_results(midj_path)
    dalle_results = get_error_results(dalle_path)

    return v10_results, v15_results, v21_results, midj_results, dalle_results
#step 1: get error index
def get_error_idx(results):
    idx_list = []
    i = 0
    for result in results:
        obj1 = result['obj1']
        obj2 = result['obj2']
        relation = result['relation']
        obj1_num = result['obj1_num']
        obj2_num = result['obj2_num']
        if obj1 and obj2 and relation and obj1_num and obj2_num:
            continue
        else:
            idx_list.append(i)
        i += 1
    
    return idx_list

#step 2: get cross error
def get_cross_error():
    v10_results, v15_results, v21_results, midj_results, dalle_results = get_results()
    v10_idx = get_error_idx(v10_results)
    v15_idx = get_error_idx(v15_results)
    v21_idx = get_error_idx(v21_results)
    midj_idx = get_error_idx(midj_results)
    dalle_idx = get_error_idx(dalle_results)

    cross_error = set(v10_idx) & set(v15_idx) & set(v21_idx) & set(midj_idx) & set(dalle_idx)
    return list(cross_error)

#step 3: locate PPTs
def locate_PPTs():
    cross_err = get_cross_error()
    selected_PPTs = []
    PPTs = get_PPTs('path')
    for idx in cross_err:
        current_ppt = PPTs[str(idx)]
        selected_PPTs.append(current_ppt)

    return selected_PPTs
#step 4: ablation1, ablation2, ablation3
#step 5: generate prompt
def ablation1():
    #ablation1: remove the color_attribute
    color = ['red', 'blue', 'green', 'yellow', 'black', 'white', 'brown', 'purple', 'pink', 'orange']
    selected_PPTs = locate_PPTs()
    i = 0
    for ppt in selected_PPTs:
        obj1_attr = ppt['obj1_attr']
        obj2_attr = ppt['obj2_attr']
        for attr in obj1_attr:
            if attr in color:
                obj1_attr.remove(attr)
        for attr in obj2_attr:
            if attr in color:
                obj2_attr.remove(attr)
        ppt['obj1_attr'] = obj1_attr
        ppt['obj2_attr'] = obj2_attr
        generate_Prompt(selected_PPTs, i, 'ablation1')
        i += 1
    return selected_PPTs

def ablation2(selected_PPTs):
    #ablation2: remove the all the attribute expcept number_attribute
    number = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
    i = 0
    for ppt in selected_PPTs:
        obj1_attr = ppt['obj1_attr']
        obj2_attr = ppt['obj2_attr']
        for attr in obj1_attr:
            if attr not in number:
                obj1_attr.remove(attr)
        for attr in obj2_attr:
            if attr not in number:
                obj2_attr.remove(attr)
        ppt['obj1_attr'] = obj1_attr
        ppt['obj2_attr'] = obj2_attr
        generate_Prompt(selected_PPTs, i, 'ablation2')
        i += 1
    return selected_PPTs

def ablation3(selected_PPTs):
    #ablation3: remove the all the attribute
    i = 0
    for ppt in selected_PPTs:
        obj1_attr = []
        obj2_attr = []
        ppt['obj1_attr'] = obj1_attr
        ppt['obj2_attr'] = obj2_attr
        generate_Prompt(selected_PPTs, i, 'ablation3')
        i += 1



def save_prompt(prompt, ab):
    filepath = './files/{}_prompts.json'.format(ab)
    att = prompt
    if os.path.exists(filepath):
        with open('./files/{}_prompts.json'.format(ab), 'r') as f:
            att = json.load(f)
        att.update(prompt)
    with open('./files/{}_prompts.json'.format(ab), 'w') as f:
        json.dump(att, f)


def analyze_PPT(input_PPT):
    relation = input_PPT['relation']
    obj1 = input_PPT['obj1']
    obj2 = input_PPT['obj2']
    obj1_attr = input_PPT['obj1_attr']
    obj2_attr = input_PPT['obj2_attr']
    return relation, obj1, obj1_attr, obj2, obj2_attr

def generate_Prompt(input_PPT, idx, ab):
    relation, obj1, obj1_attr, obj2, obj2_attr = analyze_PPT(input_PPT)

    client = OpenAI(api_key=gpt_value['key'])
    system_msg = 'You are an expert in the field of prompt generation.'
    user_msg = """
        I will give you several nodes, and you need to fuse them together to form a prompt.
        the format should be attribute1 + object1 + relation + attribute2 + object2,
        for example, if the nodes are [['two','big'], 'apple', 'on top of', ['one','fancy'], 'table'], the return value can be 'Two big apple is on top of One fancy table'
        if attribute exists, the attributes are always adjectives and in the list.
        if there is a number in the attribute, always put the number in front of any other attributes.
        attribute1 is {}, object1 is {}, relation is {}, attribute2 is {}, object2 is {}
    """.format(obj1_attr, obj1, relation, obj2_attr, obj2)

    response = client.chat.completions.create(
        model = "gpt-4",
        messages=[
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg}]
    )
    prompt = response.choices[0].message.content
    prompt_pair = {idx: prompt}
    save_prompt(prompt_pair, ab)

if __name__ == "__main__":
    selected_PPTs = ablation1()
    selected_PPTs = ablation2(selected_PPTs)
    ablation3(selected_PPTs)
    print('Done!')
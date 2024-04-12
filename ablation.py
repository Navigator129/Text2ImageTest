import json
from openai import OpenAI
import os
from tqdm import tqdm

gpt_value = {"key": "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",
            "org": "org-YGi1QDMf6n1Ptr1pxMZHsYpE"}

def get_path(i):
    path1 = './files/exp{}/related_seed_prompts.json'
    path2 = './files/exp{}/unrelated_seed_prompts.json'
    path3 = './files/exp{}/related_mutate_prompts.json'
    path4 = './files/exp{}/unrelated_mutate_prompts.json'
    return path1.format(i), path2.format(i), path3.format(i), path4.format(i)

def get_PPTs(path):
    with open(path, 'r') as f:
        dict_ = json.load(f)
    PPTs = []
    for prompt_dict in dict_:
        if prompt_dict['validity'].lower() == 'valid':
            PPTs.append(prompt_dict['PPT'])
    return PPTs

def save_prompt(prompt_pair, path):
    with open(path, 'a') as f:
        json.dump(prompt_pair, f)

def filter_attr(attr):
    if 'the' in attr:
        attr = 'the'
    else:
        attr = 'one'
    return attr

#ablation 1 remove attributes
def ablation1():    
    for i in tqdm(range(3,5)):
        related_seed_path, unrelated_seed_path, related_mutate_path, unrelated_mutate_path = get_path(i)
        total_PPTs = get_PPTs(related_seed_path) + get_PPTs(unrelated_seed_path) + get_PPTs(related_mutate_path) + get_PPTs(unrelated_mutate_path)
        idx = 0
        PPT_list = []
        for PPT in tqdm(total_PPTs):
            if type(PPT) == list:
                for ppt in PPT:
                    obj1 = ppt['obj1']
                    obj2 = ppt['obj2']
                    relation = ppt['relation']
                    obj1_attr = filter_attr(ppt['obj1_attr'])
                    obj2_attr = filter_attr(ppt['obj2_attr'])
                    client = OpenAI(api_key=gpt_value['key'])
                    system_msg = 'You are an expert in the field of prompt generation.'      
                    user_msg = """
                        I will give you several nodes, and you need to fuse them together to form a prompt.
                        the format should be object1 attriubte + object1 + relation + object2 attribute + object2,
                        for example, if the nodes are 'one ', 'apple', 'on top of','one', 'table', the return value should be 'one apple is on top of one table'
                        if attribute exists, the attributes are always adjectives and in the list.
                        if there is a number in the attribute, always put the number in front of any other attributes.
                        Don't return anything but the prompt.
                        object1 attribute is {}, object1 is {}, relation is {}, object2 attribute is {}, object2 is {}
                    """.format(obj1_attr, obj1, relation, obj2_attr, obj2)

                    response = client.chat.completions.create(
                        model = "gpt-4",
                        messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": user_msg}]
                    )
                    result = response.choices[0].message.content.strip()
                    prompt = prompt + result + " "
                prompt_pair = {'idx': idx, 'prompt': prompt, 'PPT': PPT}
            else:
                obj1 = PPT['obj1']
                obj2 = PPT['obj2']
                relation = PPT['relation']
                obj1_attr = filter_attr(PPT['obj1_attr'])
                obj2_attr = filter_attr(PPT['obj2_attr'])
                client = OpenAI(api_key=gpt_value['key'])
                system_msg = 'You are an expert in the field of prompt generation.'
                user_msg = """
                    I will give you several nodes, and you need to fuse them together to form a prompt.
                    the format should be object1 attriubte + object1 + relation + object2 attribute + object2,
                    for example, if the nodes are 'one ', 'apple', 'on top of','one', 'table', the return value should be 'one apple is on top of one table'
                    if attribute exists, the attributes are always adjectives and in the list.
                    if there is a number in the attribute, always put the number in front of any other attributes.
                    Don't return anything but the prompt.
                    object1 attribute is {}, object1 is {}, relation is {}, object2 attribute is {}, object2 is {}
                """.format(obj1_attr, obj1, relation, obj2_attr, obj2)

                response = client.chat.completions.create(
                    model = "gpt-4",
                    messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}]
                )
                prompt = response.choices[0].message.content
                prompt_pair = {'idx': idx, 'prompt': prompt, 'PPT': PPT}
            PPT_list.append(prompt_pair)
            idx += 1
        path = './files/exp{}/ablation/'.format(i)
        if not os.path.exists(path):
            os.makedirs(path)
        file_path = path + 'ablation1.json'
        save_prompt(PPT_list, file_path)



def ablation2():
    for i in tqdm(range(1, 5)):
        related_seed_path, unrelated_seed_path, related_mutate_path, unrelated_mutate_path = get_path(i)
        total_PPTs = get_PPTs(related_seed_path) + get_PPTs(unrelated_seed_path) + get_PPTs(related_mutate_path) + get_PPTs(unrelated_mutate_path)
        idx = 0
        PPT_list = []
        for PPT in tqdm(total_PPTs):
            if type(PPT) == list:
                continue
            else:
                obj1 = PPT['obj1']
                obj2 = PPT['obj2']
                obj1_attr = filter_attr(PPT['obj1_attr'])
                obj2_attr = filter_attr(PPT['obj2_attr'])
                client = OpenAI(api_key=gpt_value['key'])
                system_msg = 'You are an expert in the field of prompt generation.'
                user_msg = """
                    I will give you several nodes, and you need to fuse them together to form a prompt.
                    the format should be object1 attriubte + object1 + relation + object2 attribute + object2,
                    for example, if the nodes are 'one ', 'apple', 'one', 'table', the return value should be 'one apple and one table'
                    if attribute exists, the attributes are always adjectives and in the list.
                    if there is a number in the attribute, always put the number in front of any other attributes.
                    Don't return anything but the prompt.
                    object1 attribute is {}, object1 is {}, object2 attribute is {}, object2 is {}
                """.format(obj1_attr, obj1, obj2_attr, obj2)
                response = client.chat.completions.create(
                    model = "gpt-4",
                    messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}]
                )
                prompt = response.choices[0].message.content
                prompt_pair = {'idx': idx, 'prompt': prompt, 'PPT': PPT}
                PPT_list.append(prompt_pair)
                idx += 1
        path = './files/exp{}/ablation/'.format(i)
        if not os.path.exists(path):
            os.makedirs(path)
        file_path = path + 'ablation2.json'
        save_prompt(PPT_list, file_path)

def quick_ab1():
    with open('./files/test.json', 'r') as f:
        quick_test_cases = json.load(f)
    idx = 0
    PPT_list = []
    for test_dict in tqdm(quick_test_cases):
        test_ppt = test_dict['PPT']
        if type(test_ppt) == list:
            for ppt in test_ppt:
                obj1 = ppt['obj1']
                obj2 = ppt['obj2']
                relation = ppt['relation']
                obj1_attr = filter_attr(ppt['obj1_attr'])
                obj2_attr = filter_attr(ppt['obj2_attr'])
                client = OpenAI(api_key=gpt_value['key'])
                system_msg = 'You are an expert in the field of prompt generation.'      
                user_msg = """
                    I will give you several nodes, and you need to fuse them together to form a prompt.
                    the format should be object1 attriubte + object1 + relation + object2 attribute + object2,
                    for example, if the nodes are 'one ', 'apple', 'on top of','one', 'table', the return value should be 'one apple is on top of one table'
                    if attribute exists, the attributes are always adjectives and in the list.
                    if there is a number in the attribute, always put the number in front of any other attributes.
                    Don't return anything but the prompt.
                    object1 attribute is {}, object1 is {}, relation is {}, object2 attribute is {}, object2 is {}
                """.format(obj1_attr, obj1, relation, obj2_attr, obj2)

                response = client.chat.completions.create(
                    model = "gpt-4",
                    messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}]
                )
                result = response.choices[0].message.content.strip()
                prompt = prompt + result + " "
            prompt_pair = {'idx': idx, 'prompt': prompt, 'PPT': test_ppt}
        else:
            obj1 = test_ppt['obj1']
            obj2 = test_ppt['obj2']
            relation = test_ppt['relation']
            obj1_attr = filter_attr(test_ppt['obj1_attr'])
            obj2_attr = filter_attr(test_ppt['obj2_attr'])
            client = OpenAI(api_key=gpt_value['key'])
            system_msg = 'You are an expert in the field of prompt generation.'
            user_msg = """
                I will give you several nodes, and you need to fuse them together to form a prompt.
                the format should be object1 attriubte + object1 + relation + object2 attribute + object2,
                for example, if the nodes are 'one ', 'apple', 'on top of','one', 'table', the return value should be 'one apple is on top of one table'
                if attribute exists, the attributes are always adjectives and in the list.
                if there is a number in the attribute, always put the number in front of any other attributes.
                object1 attribute is {}, object1 is {}, relation is {}, object2 attribute is {}, object2 is {}
            """.format(obj1_attr, obj1, relation, obj2_attr, obj2)

            response = client.chat.completions.create(
                model = "gpt-4",
                messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}]
            )
            prompt = response.choices[0].message.content
            prompt_pair = {'idx': idx, 'prompt': prompt, 'PPT': test_ppt}
        PPT_list.append(prompt_pair)
        idx += 1
    path = './files/'
    file_path = path + 'ablation1.json'
    save_prompt(PPT_list, file_path)

def quick_ab2():
    with open('./files/test.json', 'r') as f:
        quick_test_cases = json.load(f)
    idx = 0
    PPT_list = []
    for test_ppt in tqdm(quick_test_cases):
        if type(test_ppt) == list:
            for ppt in test_ppt:
                obj1 = ppt['obj1']
                obj2 = ppt['obj2']
                client = OpenAI(api_key=gpt_value['key'])
                system_msg = 'You are an expert in the field of prompt generation.'      
                user_msg = """
                    I will give you several nodes, and you need to fuse them together to form a prompt.
                    the format should be object1 attriubte + object1 + relation + object2 attribute + object2,
                    for example, if the nodes are 'one ', 'apple', 'one', 'table', the return value should be 'one apple and one table'
                    if attribute exists, the attributes are always adjectives and in the list.
                    if there is a number in the attribute, always put the number in front of any other attributes.
                    object1 is {}, object2 is {}
                """.format(obj1_attr, obj1, obj2_attr, obj2)
                response = client.chat.completions.create(
                    model = "gpt-4",
                    messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}]
                )
                result = response.choices[0].message.content.strip()
                prompt = prompt + result + " "
            prompt_pair = {'idx': idx, 'prompt': prompt, 'PPT': test_ppt}
        else:
            obj1 = test_ppt['obj1']
            obj2 = test_ppt['obj2']
            obj1_attr = filter_attr(test_ppt['obj1_attr'])
            obj2_attr = filter_attr(test_ppt['obj2_attr'])
            client = OpenAI(api_key=gpt_value['key'])
            system_msg = 'You are an expert in the field of prompt generation.'
            user_msg = """
                I will give you several nodes, and you need to fuse them together to form a prompt.
                the format should be object1 attriubte + object1 + relation + object2 attribute + object2,
                for example, if the nodes are 'one ', 'apple', 'one', 'table', the return value should be 'one apple and one table'
                if attribute exists, the attributes are always adjectives and in the list.
                if there is a number in the attribute, always put the number in front of any other attributes.
                object1 attribute is {}, object1 is {}, object2 attribute is {}, object2 is {}
            """.format(obj1_attr, obj1, obj2_attr, obj2)
            response = client.chat.completions.create(
                model = "gpt-4",
                messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}]
            )
            prompt = response.choices[0].message.content
            prompt_pair = {'idx': idx, 'prompt': prompt, 'PPT': test_ppt}
            PPT_list.append(prompt_pair)
            idx += 1
    path = './files/'
    file_path = path + 'ablation2.json'
    save_prompt(PPT_list, file_path)

                

if __name__ == "__main__":
    # ablation1()
    # print('finish ablation1')
    # ablation2()
    # print('finish ablation2')
    quick_ab1()
    print('finish quick_ab1')
    quick_ab2()
    print('finish quick_ab2')
import json
import os
from openai import OpenAI
from mutatePPT import *
from constructPPT import *
from tqdm import tqdm


gpt_value = {"key": "sk-proj-1BPvHk5XzjyLbAc1UPy5T3BlbkFJSuwD9Ey30jzLFHcL30ZD",
            "org": "YOUR_ORG_ID",}

def analyze_PPT(input_PPT):
    #analyze the PPT and return the object and the attributes
    M_check = input_PPT.value
    if M_check:
        relation_nodes = input_PPT.get_children()
        subtrees = []
        for relation_node in relation_nodes:
            obj1 = relation_node.get_children()[0]
            obj2 = relation_node.get_children()[1]
            attr1 = obj1.get_children()
            attr2 = obj2.get_children()
            obj1_attr = get_attribute_values(attr1)
            obj2_attr = get_attribute_values(attr2)
            subtree = construct_PPT_dict(relation_node.value, obj1.value, obj1_attr, obj2.value, obj2_attr)
            subtrees.append(subtree)
        return subtrees
    else:
        relation_node = input_PPT.get_children()[0]
        obj1 = relation_node.get_children()[0]
        obj2 = relation_node.get_children()[1]
        attr1 = obj1.get_children()
        attr2 = obj2.get_children()
        obj1_attr = get_attribute_values(attr1)
        obj2_attr = get_attribute_values(attr2)
        subtree = construct_PPT_dict(relation_node.value, obj1.value, obj1_attr, obj2.value, obj2_attr)
        return subtree


def save_prompt(prompt, related, type_):
    if related:
        save_related_prompt(prompt, type_)
    else:
        save_unrelated_prompt(prompt, type_)


def save_unrelated_prompt(prompt, type_):
    if type_ == 'seed':
        filepath = './files/unrelated_seed_prompts.json'
    else:
        filepath = './files/unrelated_mutate_prompts.json'
    att = prompt
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            att = json.load(f)
        att += prompt
    with open(filepath, 'w') as f:
        json.dump(att, f)

def save_related_prompt(prompt, type_):
    if type_ == 'seed':
        filepath = './files/related_seed_prompts.json'
    else:
        filepath = './files/related_mutate_prompts.json'
    att = prompt
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            att = json.load(f)
        att += prompt
    with open(filepath, 'w') as f:
        json.dump(att, f)

def construct_PPT_dict(relation, obj1, obj1_attr, obj2, obj2_attr):
    PPT = {}
    PPT['relation'] = relation
    PPT['obj1'] = obj1
    PPT['obj1_attr'] = obj1_attr
    PPT['obj2'] = obj2
    PPT['obj2_attr'] = obj2_attr
    return PPT


def get_attribute_values(input_PPT):
    obj_attr = []
    for attr in input_PPT:
        obj_attr.append(attr.value)
    return obj_attr

def change_article(prev_obj1, prev_obj2, obj1, obj2, subtree):
    obj1_attr = subtree['obj1_attr']
    obj2_attr = subtree['obj2_attr']
    if prev_obj1 == obj1 or prev_obj2 == obj1:
        obj1_attr.remove('one')
        obj1_attr.append('the')
                
    if prev_obj2 == obj2 or prev_obj1 == obj2:
        obj2_attr.remove('one')
        obj2_attr.append('the')

    return obj1_attr, obj2_attr


def generatePrompt(input_PPT, idx, related, type_):
    client = OpenAI(api_key=gpt_value['key'])
    system_msg = 'You are an expert in the field of prompt generation.'
    M_check = input_PPT.value
    if M_check:
        subtrees = analyze_PPT(input_PPT)
        i = 0
        prompt = ""
        for subtree in subtrees:
            relation = subtree['relation']
            obj1 = subtree['obj1']
            obj1_attr = subtree['obj1_attr']
            obj2 = subtree['obj2']
            obj2_attr = subtree['obj2_attr']
            if i == 0:
                user_msg_input = """
                I will give you several nodes, and you need to fuse them together to form a prompt.
                the format should be attribute1 + object1 + relation + attribute2 + object2,
                for example, if the nodes are [['one','big'], 'apple', 'on top of', ['one','fancy'], 'table'], the return value should be:  
                Two big apple is on top of One fancy table
                the attributes are always adjectives and in the list.
                Always put the number in front of any other attributes.
                Don't return anything but the prompt.
                attribute1 is {}, object1 is {}, relation is {}, attribute2 is {}, object2 is {}
                """.format(obj1_attr, obj1, relation, obj2_attr, obj2)
                i += 1
            else:
                obj1_attr, obj2_attr = change_article(prev_obj1, prev_obj2, obj1, obj2, subtree)
                user_msg_input = """
                I will give you several nodes, and you need to fuse them together to form a prompt.
                the format should be attribute1 + object1 + relation + attribute2 + object2,
                for example, if the nodes are [['the', 'big'], 'apple', 'on top of', ['one','fancy'], 'table'], the return value should be:
                The big apple is on top of One fancy table
                the attributes are always adjectives and in the list.
                Always put the number in front of any other attributes if there is.
                Always put 'the' in front of the any other attributes if there is.
                Don't return anything but the prompt.
                attribute1 is {}, object1 is {}, relation is {}, attribute2 is {}, object2 is {}
                """.format(obj1_attr, obj1, relation, obj2_attr, obj2)
            prev_obj1 = obj1
            prev_obj2 = obj2
            
            response = client.chat.completions.create(
            model = "gpt-4",
            messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg_input}]
            )
            result = response.choices[0].message.content.strip()
            prompt = prompt + result + " "
        prompt_pair = [{'idx': idx, 'prompt': prompt, 'PPT': subtrees}]
    else:
        subtree = analyze_PPT(input_PPT)
        relation = subtree['relation']
        obj1 = subtree['obj1']
        obj1_attr = subtree['obj1_attr']
        obj2 = subtree['obj2']
        obj2_attr = subtree['obj2_attr']
        user_msg = """
            I will give you several nodes, and you need to fuse them together to form a prompt.
            the format should be attribute1 + object1 + relation + attribute2 + object2,
            for example, if the nodes are [['one','big'], 'apple', 'on top of', ['one','fancy'], 'table'], the return value should be:  
            One big apple is on top of One fancy table
            the attributes are always adjectives and in the list.
            Always put the number in front of any other attributes.
            Don't return anything but the prompt.
            attribute1 is {}, object1 is {}, relation is {}, attribute2 is {}, object2 is {}
        """.format(obj1_attr, obj1, relation, obj2_attr, obj2)


        response = client.chat.completions.create(
            model = "gpt-4",
            messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}]
        )
        prompt = response.choices[0].message.content
        prompt_pair = [{'idx': idx, 'prompt': prompt, 'PPT': subtree}]
    if related:
        save_related_prompt(prompt_pair, type_)
    else:
        save_unrelated_prompt(prompt_pair, type_)

def generate_seed(related):
    ppt_list = []
    total_seed = 200
    for i in range(total_seed):
        if related:
            ppt = constructRelatedPPT()
        else:
            ppt = constructUnrelatedPPT()
        ppt_list.append(ppt)
    
    i = 0
    for ppt in tqdm(ppt_list):
        if related:
            generatePrompt(ppt, i, True, 'seed')
        else:
            generatePrompt(ppt, i, False, 'seed')
        i += 1
    
    return ppt_list

def check_valid(path):
    with open(path) as f:
        prompt_dicts = json.load(f)
    client = OpenAI(api_key=gpt_value['key'])
    sys_msg = "You are an expert in the field of prompt valid check."
    result_list = []
    for prompt_dict in prompt_dicts:
        prompt = prompt_dict['prompt']
        usr_msg = """
            I will offer you a prompt and you need to check if the location relation is valid or not. for example,
            'an apple is on top of a table' is valid, 'a table is on an apple' is invalid.
            The return value should be a simple 'valid' or 'invalid', even if there are multiple sets in the prompt.
            This is the prompt: {}
        """.format(prompt)
        response = client.chat.completions.create(
            model = "gpt-4",
            messages=[
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": usr_msg}]
        )
        result = response.choices[0].message.content.strip()
        prompt_dict['validity'] = result
        result_list.append(prompt_dict)
    with open(path, 'w') as f:
        json.dump(result_list, f)
    return result_list

if __name__ == "__main__":
    related_seed_ppt = generate_seed(True)
    unrelated_seed_ppt = generate_seed(False)
    related_seed_prompt = './files/related_seed_prompts.json'
    unrelated_seed_prompt = './files/unrelated_seed_prompts.json'

    related_seed_result = check_valid(related_seed_prompt)
    unrelated_seed_result = check_valid(unrelated_seed_prompt)

    i = 0
    related_mutate_tree = []
    for related_seed in related_seed_result:
        if related_seed['validity'].lower() == 'valid':
            idx = related_seed['idx']
            input_PPT = related_seed_ppt[idx]
            mutate_tree = mutator(input_PPT, True)
            related_mutate_tree += mutate_tree

    unrelated_mutate_tree = []
    for unrelated_seed in unrelated_seed_result:
        if unrelated_seed['validity'].lower() == 'valid':
            idx = unrelated_seed['idx']
            input_PPT = unrelated_seed_ppt[idx]
            mutate_tree = mutator(input_PPT, False)
            unrelated_mutate_tree += mutate_tree
    i = 0
    for ppt in tqdm(related_mutate_tree):
        generatePrompt(ppt, i, True, 'mutate')
        i += 1
    i = 0
    for ppt in tqdm(unrelated_mutate_tree):
        generatePrompt(ppt, i, False, 'mutate')
        i += 1

    # check_valid('./files/related_mutate_prompts.json')
    # check_valid('./files/unrelated_mutate_prompts.json')

    print("Done!")
    
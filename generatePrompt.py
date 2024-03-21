import json
import os
import re
from openai import OpenAI

gpt_value = {"key": "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",
            "org": "org-YGi1QDMf6n1Ptr1pxMZHsYpE"}

def analyze_PPT(input_PPT):
    #analyze the PPT and return the object and the attributes
    obj1 = input_PPT.get_children()[0]
    obj2 = input_PPT.get_children()[1]
    attr1 = obj1.get_children()
    attr2 = obj2.get_children()
    obj1_attr = get_attribute_values(attr1)
    obj2_attr = get_attribute_values(attr2)
    return input_PPT.value, obj1.value, obj1_attr, obj2.value, obj2_attr


def save_prompt(prompt):
    filepath = './files/prompts.json'
    att = prompt
    if os.path.exists(filepath):
        with open('./files/prompts.json', 'r') as f:
            att = json.load(f)
        att.update(prompt)
    with open('./files/prompts.json', 'w') as f:
        json.dump(att, f)

def save_PPT(dict_):
    list_ = []
    filepath = './files/PPTs.json'

    if os.path.exists(filepath):
        with open('./files/PPTs.json', 'r') as f:
            list_ = json.load(f)
        list_.append(dict_)
    else:
        list_.append(dict_)
    with open('./files/PPTs.json', 'w') as f:
        json.dump(list_, f)

def get_attribute_values(input_PPT):
    obj_attr = []
    for attr in input_PPT:
        obj_attr.append(attr.value)
    return obj_attr

def generatePrompt(input_PPT, idx):
    PPT = {}
    relation, obj1, obj1_attr, obj2, obj2_attr = analyze_PPT(input_PPT)
    PPT['relation'] = relation
    PPT['obj1'] = obj1
    PPT['obj1_attr'] = obj1_attr
    PPT['obj2'] = obj2
    PPT['obj2_attr'] = obj2_attr
    save_PPT(PPT)

    client = OpenAI(api_key=gpt_value['key'])
    system_msg = 'You are an expert in the field of prompt generation.'
    user_msg = """
        I will give you several nodes, and you need to fuse them together to form a prompt.
        the format should be attribute1 + object1 + relation + attribute2 + object2,
        for example, if the nodes are [['two','big'], 'apple', 'on top of', ['one','fancy'], 'table'], the return value can be 'Two big apple is on top of One fancy table'
        the attributes are always adjectives and in the list.
        Always put the number in front of any other attributes.
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
    save_prompt(prompt_pair)

    
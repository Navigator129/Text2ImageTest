import json
import os
from openai import OpenAI
from mutatePPT import *
from constructPPT import *
from tqdm import tqdm


gpt_value = {"key": "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",
            "org": "org-YGi1QDMf6n1Ptr1pxMZHsYpE"}

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
            subtree = construct_PPT_dict(input_PPT.value, obj1.value, obj1_attr, obj2.value, obj2_attr)
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
        subtree = construct_PPT_dict(input_PPT.value, obj1.value, obj1_attr, obj2.value, obj2_attr)
        return subtree


def save_prompt(prompt, related):
    if related:
        save_related_prompt(prompt)
    else:
        save_unrelated_prompt(prompt)


def save_unrelated_prompt(prompt):
    filepath = './files/unrelated_prompts.json'
    att = prompt
    if os.path.exists(filepath):
        with open('./files/unrelated_prompts.json', 'r') as f:
            att = json.load(f)
        att.update(prompt)
    with open('./files/unrelated_prompts.json', 'w') as f:
        json.dump(att, f)

def save_related_prompt(prompt):
    filepath = './files/related_prompts.json'
    att = prompt
    if os.path.exists(filepath):
        with open('./files/related_prompts.json', 'r') as f:
            att = json.load(f)
        att.update(prompt)
    with open('./files/related_prompts.json', 'w') as f:
        json.dump(att, f)

def construct_PPT_dict(relation, obj1, obj1_attr, obj2, obj2_attr):
    PPT = {}
    PPT['relation'] = relation
    PPT['obj1'] = obj1
    PPT['obj1_attr'] = obj1_attr
    PPT['obj2'] = obj2
    PPT['obj2_attr'] = obj2_attr
    return PPT


def save_PPT(dict_, related):
    list_ = []
    if related:
        filepath = './files/related_PPTs.json'
    else:
        filepath = './files/unrelated_PPTs.json'

    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            list_ = json.load(f)
        list_.append(dict_)
    else:
        list_.append(dict_)
    with open(filepath, 'w') as f:
        json.dump(list_, f)

def get_attribute_values(input_PPT):
    obj_attr = []
    for attr in input_PPT:
        obj_attr.append(attr.value)
    return obj_attr

def generatePrompt(input_PPT, idx, related):
    client = OpenAI(api_key=gpt_value['key'])
    system_msg = 'You are an expert in the field of prompt generation.'
    M_check = input_PPT.value
    if M_check:
        subtrees = analyze_PPT(input_PPT)
        save_PPT(subtrees, related)
        total_subtree = len(subtrees)
        user_msg_base = """
            I will offer you {} sets of nodes and you need to fuse them together to form a prompt.
            each set is consist of one relation node, two object nodes obj1 and obj2, and corresponding attribute nodes for each obj.
            you need to combine the five nodes together, in a format of attribute1 + object1 + relation + attribute2 + object2.
            for example, if the nodes are [['one','big'], 'apple', 'on top of', ['one','fancy'], 'table'], the return value can be 'Two big apple is on top of One fancy table'
            the attributes are always adjectives and in the list.
            Always put the number in front of any other attributes.
        """.format(total_subtree)
        user_msg_cont = """
            the obj in different sets are related, if obj1 and obj2 in the first set is 'apple' and 'table', and obj1 and obj2 in the second set is 'banana' and 'apple',
            then prompt you generate should be 'one apple is relation one table, one banana is relation the apple' to emphasize the apple in both sentences are the same apple.
        """
        for subtree in subtrees:
            relation = subtree['relation']
            obj1 = subtree['obj1']
            obj1_attr = subtree['obj1_attr']
            obj2 = subtree['obj2']
            obj2_attr = subtree['obj2_attr']
            user_msg_input = """
            relation: {}, obj1: {}, obj_attr1: {}, obj2: {}, obj_attr2: {}
        """.format(relation, obj1, obj1_attr, obj2, obj2_attr)

            response = client.chat.completions.create(
            model = "gpt-4",
            messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg_base},
            {"role": "user", "content": user_msg_cont},
            {"role": "user", "content": user_msg_input}]
            )
            prompt = response.choices[0].message.content
            time.sleep(0.5)
    else:
        subtree = analyze_PPT(input_PPT)
        save_PPT(subtree, related)
        relation = subtree['relation']
        obj1 = subtree['obj1']
        obj1_attr = subtree['obj1_attr']
        obj2 = subtree['obj2']
        obj2_attr = subtree['obj2_attr']
        user_msg = """
            I will give you several nodes, and you need to fuse them together to form a prompt.
            the format should be attribute1 + object1 + relation + attribute2 + object2,
            for example, if the nodes are [['one','big'], 'apple', 'on top of', ['one','fancy'], 'table'], the return value can be 'Two big apple is on top of One fancy table'
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
        time.sleep(0.5)
    prompt_pair = {idx: prompt}
    if related:
        save_related_prompt(prompt_pair)
    else:
        save_unrelated_prompt(prompt_pair)

if __name__ == "__main__":
    unrelated_ppt_list = []
    for i in tqdm(range(1)):
        ppt = constructUnrelatedPPT()
        unrelated_ppt_list.append(ppt)
        mutate_tree = mutator(ppt)
        unrelated_ppt_list = unrelated_ppt_list + mutate_tree
    
    for ppt in tqdm(unrelated_ppt_list):
        mutate_tree = mutator(ppt)
        unrelated_ppt_list = unrelated_ppt_list + mutate_tree
   
    related_ppt_list = []
    for i in tqdm(range(1)):
        ppt = constructRelatedPPT()
        related_ppt_list.append(ppt)
        mutate_tree = mutator(ppt)
        related_ppt_list = related_ppt_list + mutate_tree

    for ppt in tqdm(related_ppt_list):
        mutate_tree = mutator(ppt)
        related_ppt_list = related_ppt_list + mutate_tree

    i = 0
    for ppt in tqdm(unrelated_ppt_list):
        generatePrompt(ppt, i, False)
        i += 1
    i = 0
    for ppt in tqdm(related_ppt_list):
        generatePrompt(ppt, i, True)
        i += 1

    print("Done!")
    
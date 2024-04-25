import json
import os
import re
from openai import OpenAI

gpt_value = {"key": "YOUR_API_KEY",
            "org": "YOUR_ORG_ID",}

with open('./files/object_datasets.json', 'r') as f:
    objects = json.load(f)

def format_prompt(str_):
    if "'" in str_:
        str_ = str_.replace("'", "")
    return str_

def save_attribute(obj_att):
    filepath = './files/attribute_datasets.json'
    att = obj_att
    if os.path.exists(filepath):
        with open('./files/attribute_datasets.json', 'r') as f:
            att = json.load(f)
        att.update(obj_att)
    with open('./files/attribute_datasets.json', 'w') as f:
        json.dump(att, f)

def get_attribute_values():
    client = OpenAI(api_key=gpt_value['key'])
    system_msg = 'You are an expert in the field of attaching attributes to objects.'
    for obj_list in objects.values():
        for obj in obj_list:
            user_msg = """
                I give you an object and you need to attach three attributes of the object.
                For example, if the object is a car, the return value can be ['big', 'expensive', 'dirty']
                The attributes are adjectives that describe the object.
                Don't use colors and numbers as attributes.
                The object is a {}
            """.format(obj)

            response = client.chat.completions.create(
                model = "gpt-4",
                messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}]
            )
            attribute = response.choices[0].message.content
            attribute = format_prompt(attribute)
            obj_att = {obj: attribute} 
            save_attribute(obj_att)

def parse_attribute_values():
    with open('./files/attribute_datasets.json', 'r') as f:
        att = json.load(f)
    
    for key in att.keys():
        values = att[key]
        words_list = re.split('\[|\]|, ', values)
        words_list = [word for word in words_list if word]#delete empty strings
        att[key] = words_list
    with open('./files/attribute_datasets.json', 'w') as f:
        json.dump(att, f)

if __name__ == "__main__":
    # get_attribute_values()
    parse_attribute_values()
    
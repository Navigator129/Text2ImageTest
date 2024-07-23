import json

file_path  = '/Users/yifanhuang/workspace/Text2ImageTest/files/unrelated_mutate_prompts.json'
with open(file_path, 'r') as f:
    datalist = json.load(f)

new_result = []
for data in datalist:
    prompt = data['prompt']
    idx = data['idx']
    new_dict = {idx: prompt}
    new_result.append(new_dict)

with open('optimal.json', 'w') as f:
    json.dump(new_result, f, indent=4)
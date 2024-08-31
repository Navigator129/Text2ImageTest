import json

file_path  = '/Users/yifanhuang/workspace/Text2ImageTest/files/exp{}/related_seed_prompts.json'
for i in range(1, 6):
    file_path = file_path.format(i)
    with open(file_path, 'r') as f:
        datalist = json.load(f)

    new_result = []
    for data in datalist:
        prompt = data['prompt']
        idx = data['idx']
        if 'left' in prompt or 'right' in prompt:
            continue
        new_dict = {idx: prompt}
        new_result.append(new_dict)

    with open('related_seed_set_{}.json'.format(i), 'w') as f:
        json.dump(new_result, f, indent=4)
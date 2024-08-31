import json

file_path1 = "./files/exp{}/related_seed_prompts.json".format(1)
file_path2 = "./files/exp{}/unrelated_seed_prompts.json".format(1)
file_path3 = "./files/exp{}/related_mutate_prompts.json".format(1)
file_path4 = "./files/exp{}/unrelated_mutate_prompts.json".format(1)

for i in range(4):
    file_path = eval('file_path{}'.format(i+1))
    final_data = []
    with open(file_path, 'r') as f:
        datalist = json.load(f)
        for data in datalist:
            if data['validity'] == True:
                final_data.append(data)
            else:
                continue
    
    i = 0
    for data in final_data:
        data['idx'] = i
        i += 1

    with open(file_path, 'w') as f:
        json.dump(final_data, f, indent=4)
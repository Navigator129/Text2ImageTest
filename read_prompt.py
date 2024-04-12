import json
import pandas as pd

def read_json(file_path):
    """Reads a JSON file and returns its content."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    result = []
    for prompt_dict in data:
        if prompt_dict['validity'].lower() == 'valid':
            result.append(prompt_dict['prompt'])
    return result

def get_whole_prompts_with_PPTs(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    result = []
    for prompt_dict in data:
        new_dict_ = {}
        if prompt_dict['validity'].lower() == 'valid':
            new_dict_['prompt'] = prompt_dict['prompt']
            new_dict_['PPT'] = prompt_dict['PPT']
            result.append(new_dict_)
    return result

def save_json(data, file_path):
    """Saves the data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f)


def match_PPTs():
    #find the quick_test prompts's PPT
    file_path = './files/exp{}/'.format(1)
    related_seed_path = file_path + 'related_seed_prompts.json'
    unrelated_seed_path = file_path + 'unrelated_seed_prompts.json'
    related_mutate_path = file_path + 'related_mutate_prompts.json'
    unrelated_mutate_path = file_path + 'unrelated_mutate_prompts.json'
    #total_list: save all the prompts with PPTs
    total_list = get_whole_prompts_with_PPTs(related_seed_path) + get_whole_prompts_with_PPTs(unrelated_seed_path) + get_whole_prompts_with_PPTs(related_mutate_path) + get_whole_prompts_with_PPTs(unrelated_mutate_path)
    #total_prompts: save all the prompts, used to find the index of quci_test prompts
    with open('./files/exp1/prompts.json', 'r') as f:
        total_prompts = json.load(f)
    with open('./files/quick_test.json', 'r') as f:
        quick_test_prompts = json.load(f)

    result = []
    quick_test_prompts_list = quick_test_prompts['Prompts']
    for i in range(100):
        prompt = quick_test_prompts_list[str(i)]
        idx = total_prompts.index(prompt)
        new_dict_ = total_list[idx]
        new_dict_['idx'] = i
        result.append(total_list[idx])
    
    save_json(result, './files/test.json')
        



def convert_json_to_df(data):
    """Converts JSON data into a pandas DataFrame."""
    # Convert the dictionary into a list of tuples with (index, prompt), then create a DataFrame
    i = 0
    dict_ = {}
    for prompt in data:
        dict_[i] = prompt
        i += 1
    index_prompt_pairs = [(k, v) for k, v in dict_.items()]
    df = pd.DataFrame(index_prompt_pairs, columns=['Index', 'Prompts'])
    return df

def create_excel_file(df, file_path):
    """Saves the DataFrame to an Excel file."""
    df.to_excel(file_path, index=False)

def convert_excel_to_json(path):
    """Converts an Excel file to a JSON file."""
    df = pd.read_excel(path)
    data = df.to_dict()
    with open(path.replace('.xlsx', '.json'), 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    match_PPTs()
    # for i in range(1, 5):
    #     final_data = []
    #     file_path = './files/exp{}/'.format(i)
    #     related_seed_path = file_path + 'related_seed_prompts.json'
    #     unrelated_seed_path = file_path + 'unrelated_seed_prompts.json'
    #     related_mutate_path = file_path + 'related_mutate_prompts.json'
    #     unrelated_mutate_path = file_path + 'unrelated_mutate_prompts.json'
    #     related_seed_data = read_json(related_seed_path)
    #     unrelated_seed_data = read_json(unrelated_seed_path)
    #     related_mutate_data = read_json(related_mutate_path)
    #     unrelated_mutate_data = read_json(unrelated_mutate_path)
    #     final_data.extend(related_seed_data)
    #     final_data.extend(unrelated_seed_data)
    #     final_data.extend(related_mutate_data)
    #     final_data.extend(unrelated_mutate_data)

    #     save_json(final_data, file_path + 'prompts.json')

    # convert_excel_to_json('./files/quick_test.xlsx')
        # data_df = convert_json_to_df(final_data)
        # create_excel_file(data_df, './files/exp{}/prompts.xlsx'.format(i))

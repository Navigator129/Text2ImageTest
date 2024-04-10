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

if __name__ == '__main__':
    for i in range(1, 5):
        final_data = []
        file_path = './files/exp{}/'.format(i)
        related_seed_path = file_path + 'related_seed_prompts.json'
        unrelated_seed_path = file_path + 'unrelated_seed_prompts.json'
        related_mutate_path = file_path + 'related_mutate_prompts.json'
        unrelated_mutate_path = file_path + 'unrelated_mutate_prompts.json'
        related_seed_data = read_json(related_seed_path)
        unrelated_seed_data = read_json(unrelated_seed_path)
        related_mutate_data = read_json(related_mutate_path)
        unrelated_mutate_data = read_json(unrelated_mutate_path)
        final_data.extend(related_seed_data)
        final_data.extend(unrelated_seed_data)
        final_data.extend(related_mutate_data)
        final_data.extend(unrelated_mutate_data)
        data_df = convert_json_to_df(final_data)
        create_excel_file(data_df, './files/exp{}/prompts.xlsx'.format(i))

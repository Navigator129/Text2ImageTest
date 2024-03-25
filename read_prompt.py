import json
import pandas as pd

def read_json(file_path):
    """Reads a JSON file and returns its content."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def convert_json_to_df(data):
    """Converts JSON data into a pandas DataFrame."""
    # Convert the dictionary into a list of tuples with (index, prompt), then create a DataFrame
    index_prompt_pairs = [(k, v) for k, v in data.items()]
    df = pd.DataFrame(index_prompt_pairs, columns=['Index', 'Prompts'])
    return df

def create_excel_file(df, file_path='output.xlsx'):
    """Saves the DataFrame to an Excel file."""
    df.to_excel(file_path, index=False)

if __name__ == '__main__':
    file_path = './files/prompts.json'
    json_data = read_json(file_path)
    data_df = convert_json_to_df(json_data)
    create_excel_file(data_df)

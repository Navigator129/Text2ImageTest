import json
import pandas as pd

def fetch_prompt(file_path):
    prompts = []
    with open(file_path, "r") as file:
        data = json.load(file)
    for dict_ in data:
        prompts.append(dict_["prompt"])
    return prompts


def generate_excel_midj(prompts, save_path):
    #used to create excel file for midjourney
    df = pd.DataFrame({
        'Index': range(len(prompts)),
        'Prompt': prompts,
        'P1': '',
        'P2': '',
        'P3': '',
        'P4': ''
    })
    df.to_excel(save_path, index=False)

def generate_excel(prompts, save_path):
    #used to create excel file for other experiments
    df = pd.DataFrame({
        'Index': range(len(prompts)),
        'Prompt': prompts,
        'Pic': ''
    })
    df.to_excel(save_path, index=False)

if __name__ == "__main__":
    for i in range(1,4):
        file_path1 = './files/exp{}/related_seed_prompts.json'.format(i)
        file_path2 = './files/exp{}/related_mutate_prompts.json'.format(i)
        file_path3 = './files/exp{}/unrelated_seed_prompts.json'.format(i)
        file_path4 = './files/exp{}/unrelated_mutate_prompts.json'.format(i)
        prompt_list1 = fetch_prompt(file_path1)
        prompt_list2 = fetch_prompt(file_path2)
        prompt_list3 = fetch_prompt(file_path3)
        prompt_list4 = fetch_prompt(file_path4)
        
        related_prompts = prompt_list1 + prompt_list2
        unrelated_prompts = prompt_list3 + prompt_list4

        generate_excel_midj(related_prompts, './files/excels/exp{}/midj_related_prompts.xlsx'.format(i))
        generate_excel_midj(unrelated_prompts, './files/excels/exp{}/midj_unrelated_prompts.xlsx'.format(i))

        generate_excel(related_prompts, './files/excels/exp{}/related_prompts.xlsx'.format(i))
        generate_excel(unrelated_prompts, './files/excels/exp{}/unrelated_prompts.xlsx'.format(i))



import json
from midj_generator import compensate
from tqdm import tqdm

def get_initial_prompt(path):
    with open(path, 'r') as f:
        prompts = json.load(f)
    return prompts['Prompts']

def get_ab1_prompt(path):
    with open(path, 'r') as f:
        prompts = json.load(f)
    return prompts

def process_initial():
    input_prompts = get_initial_prompt('./files/quick_test.json')
    channel_id = 1228428338175938661
    for i in tqdm(range(100)):
        prompt = input_prompts[str(i)]
        compensate(prompt, channel_id)

def process_ab1():
    input_prompts = get_ab1_prompt('./files/ablation1.json')
    channel_id = 1228454981842243846
    for p in tqdm(input_prompts):
        prompt = p['prompt']
        compensate(prompt, channel_id)

def process_ab2():
    input_prompts = get_ab1_prompt('./files/ablation2.json')
    channel_id = 1228486512325165198
    for p in tqdm(input_prompts[:5]):
        prompt = p['prompt']
        compensate(prompt, channel_id)

if __name__ == '__main__':
    # process_initial()
    # process_ab1()
    process_ab2()
    print('done')


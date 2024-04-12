import json
import midj_generator as mg
Channel_id = [1227208194980577331, 1227352229342740521, 1227266572540973157]
def get_prompts(i):
    file_path = './files/exp{}/prompts.json'.format(i)
    with open(file_path, 'r') as f:
        prompts = json.load(f)
    return prompts


def compensate_img():
    for i in range(2,5):
        file_path = './files/missing_idx_{}.json'.format(i)
        channel_id = Channel_id[i-2]
        with open(file_path, 'r') as f:
            idx = json.load(f)
        prompts = get_prompts(i)
        for i in idx:
            selected_prompt = prompts[i]
            mg.compensate(selected_prompt, channel_id)
    

if __name__ == '__main__':
    compensate_img()
    print('Done!')
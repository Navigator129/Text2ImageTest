import json
from diffusers import DiffusionPipeline, StableDiffusionPipeline
import torch
from tqdm import tqdm
import os


def fetch_prompt(path):
    prompts = []
    with open(path, 'r', encoding = 'utf-8') as f:
        dict_list = json.load(f)

    for dict_ in dict_list:
        prompts.append(dict_['prompt'])
    return prompts

def sd1_0_generator():
    pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
    pipe.to("cuda")
    return pipe

def sd1_4_generator():
    model_id = "CompVis/stable-diffusion-v1-4"
    device = "cuda"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to('cuda')
    return pipe

def sd1_5_generator():
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")
    return pipe

def get_prompt():
    file_path1 = './files/exp{}/related_seed_prompts.json'
    file_path2 = './files/exp{}/related_mutate_prompts.json'
    file_path3 = './files/exp{}/unrelated_seed_prompts.json'
    file_path4 = './files/exp{}/unrelated_mutate_prompts.json'

    for i in range(1,4):
        prompt_list1 = fetch_prompt(file_path1.format(i))
        prompt_list2 = fetch_prompt(file_path2.format(i))
        prompt_list3 = fetch_prompt(file_path3.format(i))
        prompt_list4 = fetch_prompt(file_path4.format(i))

        related_prompts = prompt_list1 + prompt_list2
        unrelated_prompts = prompt_list3 + prompt_list4

        return related_prompts, unrelated_prompts

def generate
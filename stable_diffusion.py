from diffusers import DiffusionPipeline
import torch
import json

def load_prompt():
    with open("./files/prompts.json", "r") as f:
        prompts = json.load(f)
    prompt_list = list(prompts.values())
    return prompt_list

def generate():
    # load both base & refiner
    base = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
    )
    base.to("cuda")
    refiner = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-refiner-1.0",
        text_encoder_2=base.text_encoder_2,
        vae=base.vae,
        torch_dtype=torch.float16,
        use_safetensors=True,
        variant="fp16",
    )
    refiner.to("cuda")

    # Define how many steps and what % of steps to be run on each experts (80/20) here
    n_steps = 40
    high_noise_frac = 0.8

    # load prompt
    prompt_list = load_prompt()
    prompt = "A majestic lion jumping from a big stone at night"

    # run both experts
    image = base(
        prompt=prompt,
        num_inference_steps=n_steps,
        denoising_end=high_noise_frac,
        output_type="latent",
    ).images
    image = refiner(
        prompt=prompt,
        num_inference_steps=n_steps,
        denoising_start=high_noise_frac,
        image=image,
    ).images[0]
    print('DONE!')

if __name__ == "__main__":
    print("Torch version:",torch.__version__)

    print("Is CUDA enabled?",torch.cuda.is_available())
    generate()

from PIL import Image
from diffusers import StableDiffusionPipeline, DiffusionPipeline
import torch
from diffusers.loaders import FromSingleFileMixin

reference_img = Image.open("result.png").convert("RGB")

def init():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using:", device)

    model_path = r"D:\Program Files\Local AI\abyssorangemix2SFW_abyssorangemix2Sfw.safetensors"
    model_path = r"D:\Program Files\Local AI\meinamix_v12Final.safetensors"
    pipe = StableDiffusionPipeline.from_single_file(
        model_path,
        torch_dtype=torch.float16,
    )
    # pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
    # pipe.load_lora_weights(r"D:\Program Files\Local AI\meinamix_v12Final.safetensors", weight=0.8)
    # pipe.load_lora_weights(r"D:\Program Files\Local AI\easynegative.safetensors", weight=0.7)
    # pipe.load_lora_weights(r"D:\Program Files\Local AI\Loraeyes_V1.safetensors", weight=0.001)
    pipe.safety_checker = None
    pipe.requires_safety_checker = False
    pipe.to(device)
    return pipe

negative = "loli, child, bad anatomy, deformed, extra limbs"


def generate(pipe, prompt: str):
    image = pipe(
        prompt=prompt,
        negative_prompt=negative,
        num_inference_steps=30,
        guidance_scale=7.5,
    ).images[0]

    global reference_img
    reference_img = image

    return image

def generate_with_reference(pipe, prompt, strength=0):
    image = pipe(
        prompt=prompt,
        negative_prompt=negative,
        image=Image.open("result.png").convert("RGB"),
        strength=strength,  
        num_inference_steps=30,
        guidance_scale=7.5,
    ).images[0]
    return image

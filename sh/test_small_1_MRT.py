import os, json
import openai
model_name = "/lustre/S/tianzikang/LLMs/mistralai-Pixtral-12B-2409/mistralai-Pixtral-12B-2409/" # gpt-4o, gpt-4-turbo
if os.path.isdir(model_name):
    model_name_split = model_name.split("/")
    log_model_name = model_name_split[-1] if model_name_split[-1] else model_name_split[-2]
else:
    log_model_name = model_name
import sys
sys.path.append(".")
if "gpt" in model_name:
    from config import openai_key
    openai.api_key = openai_key
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
    client = openai
else:
    from openai import OpenAI
    openai.api_key = "0"
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:8000'
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:8000'
    openai_api_key = "EMPTY"
    openai_api_base = "http://localhost:8000/v1"
    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )

from copy import deepcopy
from utils import encode_image, flatten
from datetime import datetime
current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
import tqdm

tasks = [
    "1_MRT",
    "2_PTT",
    "3_WLT",
    "4_MPFB",
    "5_JLO",
]

task = "1_MRT"
assert task in tasks, f"Invalid task: {task}"

task_path = os.path.join("Small_Scale", task)

prompt = open(os.path.join(task_path, "v_prompt.md"), "r").read()
# replace placeholder (images) with assets
for specific_task in tqdm.tqdm(os.listdir(task_path)):
    # if specific_task is not a directory, skip
    if not os.path.isdir(os.path.join(task_path, specific_task)):
        continue
    specific_prompt = deepcopy(prompt)
    # open image
    image_of_reference_3d_shape = encode_image(os.path.join(task_path, specific_task, "R.jpg"))
    choice_1_image = encode_image(os.path.join(task_path, specific_task, "C1.jpg"))
    choice_2_image = encode_image(os.path.join(task_path, specific_task, "C2.jpg"))
    choice_3_image = encode_image(os.path.join(task_path, specific_task, "C3.jpg"))
    choice_4_image = encode_image(os.path.join(task_path, specific_task, "C4.jpg"))
    # split specific_prompt into list of lines by:
    placeholders = [
        "<IMAGE OF REFERENCE 3D SHAPE>",
        "<CHOICE 1 IMAGE>",
        "<CHOICE 2 IMAGE>",
        "<CHOICE 3 IMAGE>",
        "<CHOICE 4 IMAGE>",
    ]
    # split specific_prompt into list of lines by placeholders and flatten
    for placeholder in placeholders:
        if isinstance(specific_prompt, str):
            specific_prompt = specific_prompt.split(placeholder)
        elif isinstance(specific_prompt, list):
            specific_prompt[-1] = specific_prompt[-1].split(placeholder)
            specific_prompt = flatten(specific_prompt)
        else:
            raise ValueError(f"Invalid type: {type(specific_prompt)}")
    
    assert len(specific_prompt) == len(placeholders) + 1, f"Invalid number of placeholders: {len(specific_prompt)}"
    # breakpoint()
    # request openai
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": specific_prompt[0]
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_of_reference_3d_shape}"}
                    },
                    {
                        "type": "text",
                        "text": specific_prompt[1]
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{choice_1_image}"}
                    },
                    {
                        "type": "text",
                        "text": specific_prompt[2]
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{choice_2_image}"}
                    },
                    {
                        "type": "text",
                        "text": specific_prompt[3]
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{choice_3_image}"}
                    },
                    {
                        "type": "text",
                        "text": specific_prompt[4]
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{choice_4_image}"}
                    },
                    {
                        "type": "text",
                        "text": specific_prompt[5]
                    }
                ]
            }
        ]
    )
    
    os.makedirs(os.path.join("logs", "Small_Scale", log_model_name, task, current_time), exist_ok=True)
    # save completion
    with open(os.path.join("logs", "Small_Scale", log_model_name, task, current_time, f"{specific_task}_completion.json"), "w") as f:
        json.dump(completion.model_dump_json(indent=4), f, indent=4)
    # save response
    with open(os.path.join("logs", "Small_Scale", log_model_name, task, current_time, f"{specific_task}_response.md"), "w") as f:
        f.write(completion.choices[0].message.content)
        
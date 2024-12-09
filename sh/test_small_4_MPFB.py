import os, json
import openai
model_name = "gpt-4o"
import sys
sys.path.append(".")
from config import openai_key
openai.api_key = openai_key
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

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

task = "4_MPFB"
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
    image_of_puzzle_pieces = encode_image(os.path.join(task_path, specific_task, "R.jpg"))
    choice_1_image = encode_image(os.path.join(task_path, specific_task, "C1.jpg"))
    choice_2_image = encode_image(os.path.join(task_path, specific_task, "C2.jpg"))
    choice_3_image = encode_image(os.path.join(task_path, specific_task, "C3.jpg"))
    choice_4_image = encode_image(os.path.join(task_path, specific_task, "C4.jpg"))
    # split specific_prompt into list of lines by:
    placeholders = [
        "<IMAGE OF PUZZLE PIECES>",
        "<IMAGE OF CHOICE 1>",
        "<IMAGE OF CHOICE 2>",
        "<IMAGE OF CHOICE 3>",
        "<IMAGE OF CHOICE 4>",
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
    breakpoint()
    # request openai
    completion = openai.chat.completions.create(
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
                        "image_url": {"url": f"data:image/jpeg;base64,{image_of_puzzle_pieces}"}
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
    
    os.makedirs(os.path.join("logs", task_path, current_time), exist_ok=True)
    # save completion
    with open(os.path.join("logs", task_path, current_time, f"{specific_task}_completion.json"), "w") as f:
        json.dump(completion.model_dump_json(), f, indent=4)
    # save response
    with open(os.path.join("logs", task_path, current_time, f"{specific_task}_response.md"), "w") as f:
        f.write(completion.choices[0].message.content)
        
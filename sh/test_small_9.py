import os, json
import openai
model_name = "gpt-4o"
import sys
sys.path.append(".")
from config import openai_key
openai.api_key = openai_key
# os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
# os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

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
    "6_SATT",
    "7_MCT",
    "8_CPTT",
    "9_SAT",
    "10_CSWM",
]

task = "9_SAT"
assert task in tasks, f"Invalid task: {task}"

task_path = os.path.join("./Small_Scale", task)

for specific_task in tqdm.tqdm(sorted(os.listdir(task_path))):
    if not os.path.isdir(os.path.join(task_path, specific_task)):
        continue
    task_id = int(specific_task)
    specific_taskid_root = os.path.join(task_path, specific_task)
    with open(os.path.join(specific_taskid_root, "prompt-template.md"), "r") as f:
        prompt_template = f.read()
    placeholders = [
        "<IMAGE OF ARRAY 1>",
        "<IMAGE OF ARRAY 2>",
        "<IMAGE OF CHOICE 1>",
        "<IMAGE OF CHOICE 2>",
        "<IMAGE OF CHOICE 3>",
        "<IMAGE OF CHOICE 4>",
    ]
    arrays = 2
    choices = 4
    image_of_arrays = [
        encode_image(os.path.join(task_path, specific_task, f"array{i + 1}.png"))
        for i in range(arrays)
    ]
    image_of_choices = [
        encode_image(os.path.join(task_path, specific_task, f"choice{i + 1}.png"))
        for i in range(choices)
    ]
    # split specific_prompt into list of lines by placeholders and flatten
    for placeholder in placeholders:
        if isinstance(prompt_template, str):
            prompt_template = prompt_template.split(placeholder)
        elif isinstance(prompt_template, list):
            prompt_template[-1] = prompt_template[-1].split(placeholder)
            prompt_template = flatten(prompt_template)
        else:
            raise ValueError(f"Invalid type: {type(prompt_template)}")
    
    assert len(prompt_template) == len(placeholders) + 1, f"Invalid number of placeholders: {len(prompt_template)}"
    # breakpoint()
    # request openai
    content = []
    for i in range(arrays):
        content += [
            {
                "type": "text",
                "text": prompt_template[i]
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_of_arrays[i]}"}
            },
        ]
    for i in range(choices):
        content += [
            {
                "type": "text",
                "text": prompt_template[i + arrays]
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_of_choices[i]}"}
            },
        ]
    completion = openai.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "user", 
                "content": content
            }
        ]
    )
    
    os.makedirs(os.path.join("logs", "Small_Scale", model_name, task, current_time), exist_ok=True)
    # save completion
    with open(os.path.join("logs", "Small_Scale", model_name, task, current_time, f"{specific_task}_completion.json"), "w") as f:
        json.dump(completion.model_dump_json(indent=4), f, indent=4)
    # save response
    with open(os.path.join("logs", "Small_Scale", model_name, task, current_time, f"{specific_task}_response.md"), "w") as f:
        f.write(completion.choices[0].message.content)
        
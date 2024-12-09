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

task = "2_PTT"
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
    image_of_objects = encode_image(os.path.join(task_path, specific_task, "R.jpg"))
    # open question_choices_answer
    with open(os.path.join(task_path, specific_task, "Q_C_A.json"), "r") as f:
        q_c_a = json.load(f)
    question = q_c_a["Question"]
    choices = q_c_a["Choices"]
    choices_str = " ".join([f"{key}) {value}" for key, value in choices.items()])
    specific_prompt = specific_prompt.split("<IMAGE OF OBJECTS>")
    specific_prompt[-1] = specific_prompt[-1].replace("<QUESTION>", question).replace("<CHOICES>", choices_str)
    
    # breakpoint()
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
                        "image_url": {"url": f"data:image/jpeg;base64,{image_of_objects}"}
                    },
                    {
                        "type": "text",
                        "text": specific_prompt[1]
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
        
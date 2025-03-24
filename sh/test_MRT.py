import os, json
import openai
# model_name = "/lustre/S/tianzikang/LLMs/mistralai-Pixtral-12B-2409/mistralai-Pixtral-12B-2409/" # gpt-4o, gpt-4-turbo
# model_name = "gpt-4o"
# model_name = "/nfs_global/S/tianzikang/LLMs/Qwen/Qwen-Qwen2.5-VL-7B-Instruct/" # ori
model_name = "../workdir/saves/Qwen2.5-VL-7B/full/mrt_blocking/checkpoint-14148/" # sft-blocking
if os.path.isdir(model_name):
    model_name_split = model_name.split("/")
    log_model_name = model_name_split[-1] if model_name_split[-1] else model_name_split[-2]
else:
    log_model_name = model_name
import sys
sys.path.append(".")
if "gpt" in model_name:
    # from config import openai_key
    openai_key = os.environ["openai_key"]
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


task = "MRT"

# task_path = os.path.join("/nfs_global/S/tianzikang/project_data/spatial_intelligence/mrt_data/")
task_path = os.path.join("./MRT/images/")

# replace placeholder (images) with assets

os.makedirs(os.path.join("logs", "MRT", log_model_name, current_time), exist_ok=True)
log_file = open(os.path.join("logs", "MRT", log_model_name, current_time, "log.md"), "w")

test_task_num = 100
for idx, specific_task in enumerate(tqdm.tqdm(os.listdir(task_path)[:test_task_num])):
    # if specific_task is not a directory, skip
    if not os.path.isdir(os.path.join(task_path, specific_task)):
        continue
    # open image
    image_of_reference_3d_shape = encode_image(os.path.join(task_path, specific_task, "ori.png"))
    choice_1_image = encode_image(os.path.join(task_path, specific_task, "A.png"))
    choice_2_image = encode_image(os.path.join(task_path, specific_task, "B.png"))
    choice_3_image = encode_image(os.path.join(task_path, specific_task, "C.png"))
    choice_4_image = encode_image(os.path.join(task_path, specific_task, "D.png"))
    def make_role_prompt(ori, A, B, C, D):
        prompt = [
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": "Here is an image of a three-dimensional shape.\n"
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{ori}"}
                    },
                    {
                        "type": "text",
                        "text": "\nWhich of these images show the same object rotated in 3D?\n",
                    },
                    {
                        "type": "text",
                        "text": "\nA.\n"
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{A}"}
                    },
                    {
                        "type": "text",
                        "text": "\nB.\n"
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{B}"}
                    },
                    {
                        "type": "text",
                        "text": "\nC.\n"
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{C}"}
                    },
                    {
                        "type": "text",
                        "text": "\nD.\n"
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{D}"}
                    },
                    {
                        "type": "text",
                        "text": "\nThink step by step. Your response should include reasoning process and answer. Reasoning process and answer are enclosed whthin <think> </think> and <answer> </answer> tags respectively, i.e., <think> reasoning process here </think>. <answer> answer here </answer>."
                    }
                ]
            }
        ]
        
        return prompt
    prompt = make_role_prompt(image_of_reference_3d_shape, choice_1_image, choice_2_image, choice_3_image, choice_4_image)
    completion = client.chat.completions.create(
        model=model_name,
        messages=prompt,
    )
        
    content = completion.choices[0].message.content
    log_file.write("-" * 20 + f"Task {idx}" + "-" * 20 + "\n")
    log_file.write(f"Response: {content}\n")
    
    student_answer_start_idx = content.find("<answer>")
    student_answer_end_idx = content.find("</answer>")
    student_answer = content[student_answer_start_idx + len("<answer>"): student_answer_end_idx]
    
    ground_answer = json.load(open(os.path.join(task_path, specific_task, "answer.json")))["answer"]
    
    if student_answer == ground_answer:
        log_file.write("Answer Correct!\n")
    else:
        log_file.write("Answer Wrong!\n")
    
    log_file.flush()
log_file.close()        
import os, re, json
import numpy as np
from prettytable import PrettyTable
small_scale_tasks = [
    "1_MRT",
    "2_PTT",
    "3_WLT",
    "4_MPFB",
    "5_JLO",
]
model_names = [
    "gpt-4o",
    "gpt-4-turbo"
]
log_dir = os.path.join("logs", "Small_Scale")

result_dict = {}
for model_name in model_names:
    result_dict[model_name] = {}
    for task in small_scale_tasks:
        result_dict[model_name][task] = {}
        # sparse ai's answer from its response
        for d in os.listdir(os.path.join(log_dir, model_name, task)):
            # continue if d is not a directory
            if not os.path.isdir(os.path.join(log_dir, model_name, task, d)):
                continue
            for res in filter(lambda x: x.endswith(".md"), os.listdir(os.path.join(log_dir, model_name, task, d))):
                specific_task = res.replace("_response.md", "")
                if result_dict[model_name][task].get(specific_task) is None:
                    result_dict[model_name][task][specific_task] = []
                with open(os.path.join(log_dir, model_name, task, d, res), "r") as f:
                    """
                        f is a text file with the following format:
                        ...
                        ```
                        {
                            "answer": 1
                        }
                        ```
                        or
                        ...
                        ```json
                        {
                            "answer": 1
                        }
                        ```
                        we need to extract the part between the triple backticks using re
                    """
                    response_ai = f.read()
                    # breakpoint()
                    for line in response_ai.split("\n"):
                        if line.strip().startswith('"answer"'):
                            # extract the answer
                            answer = re.search(r"\d+", line.strip()).group(0)
                            result_dict[model_name][task][specific_task].append(int(answer))
                            break
                    
# breakpoint()
                    
true_answer_dict = {}
# parse true answers
for task in small_scale_tasks:
    task_path = os.path.join("Small_Scale", task)
    true_answer_dict[task] = {}
    for specific_task in os.listdir(task_path):
        # if specific_task is not a directory, skip
        if not os.path.isdir(os.path.join(task_path, specific_task)):
            continue
        # find the .json file that contains the true answer
        json_file = list(filter(lambda x: x.endswith(".json"), os.listdir(os.path.join(task_path, specific_task))))
        assert len(json_file) == 1, f"Invalid number of .json files: {len(json_file)}"
        json_file = json_file[0]
        with open(os.path.join(task_path, specific_task, json_file), "r") as f:
            true_answer = json.load(f)["Answer"]
            
        true_answer_dict[task][specific_task] = int(true_answer)
        
# breakpoint()
acc_mean_dict = {}
acc_var_dict = {}
for model_name in model_names:
    acc_mean_dict[model_name] = {}
    acc_var_dict[model_name] = {}
    for task in small_scale_tasks:
        acc_mean_dict[model_name][task] = None
        acc_var_dict[model_name][task] = None
        specific_task_acc_mean_list = []
        specific_task_acc_var_list = []
        for specific_task in result_dict[model_name][task]:
            specific_task_acc_mean = np.mean(
                np.array(result_dict[model_name][task][specific_task]) == true_answer_dict[task][specific_task]
            )
            specific_task_acc_var = np.var(
                np.array(result_dict[model_name][task][specific_task]) == true_answer_dict[task][specific_task]
            )
            specific_task_acc_mean_list.append(specific_task_acc_mean)
            specific_task_acc_var_list.append(specific_task_acc_var)
        acc_mean_dict[model_name][task] = np.mean(specific_task_acc_mean_list)
        acc_var_dict[model_name][task] = np.mean(specific_task_acc_var_list)
            
# print acc_dict as a table
table = PrettyTable()
first_row = ["Model Name"]
first_row.extend(small_scale_tasks)
table.field_names = first_row
for model_name in model_names:
    row = [model_name]
    for task in small_scale_tasks:
        row.append(f"{acc_mean_dict[model_name][task]:.2f} ± {acc_var_dict[model_name][task]:.2f}")
    table.add_row(row)
    
print(table)
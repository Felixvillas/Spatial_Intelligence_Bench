import os, json, tqdm


log_path = "/nfs_global/S/tianzikang/rocky/projects/spatial_intelligence/Spatial_Intelligence_Bench/logs/MRT/gpt-4o/2025_02_25_17_08_26/log.md"
# cal accuracy
# open log_file with read mode
log_file = open(log_path, "r")
# transform log_file to a txt
log_txt = log_file.read()

task_path = os.path.join("/nfs_global/S/tianzikang/project_data/spatial_intelligence/mrt_data/")
test_task_num = 100

for idx, specific_task in enumerate(tqdm.tqdm(os.listdir(task_path)[:test_task_num])):
    # if specific_task is not a directory, skip
    if not os.path.isdir(os.path.join(task_path, specific_task)):
        continue
    ground_answer = json.load(open(os.path.join(task_path, specific_task, "answer.json")))["answer"]
    log_txt_task_start_idx = log_txt.find(f"--------------------Task {idx}--------------------")
    if idx == test_task_num - 1:
        log_txt_task_end_idx = len(log_txt)
    else:
        log_txt_task_end_idx = log_txt.find(f"--------------------Task {idx+1}--------------------")
        
    log_txt_task = log_txt[log_txt_task_start_idx + len(f"--------------------Task {idx}--------------------"): log_txt_task_end_idx]
    answer_start_idx = log_txt_task.find("<answer>")
    answer_end_idx = log_txt_task.find("</answer>")
    answer = log_txt_task[answer_start_idx + len("<answer>"): answer_end_idx]
    if answer == ground_answer:
        print(f"Task {idx} correct!")
    # else:
        # print(f"Task {idx} wrong!")
log_file.close()
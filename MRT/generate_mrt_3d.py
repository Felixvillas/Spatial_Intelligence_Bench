import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def draw_cube(ax, position):
    # Define the vertices of a unit cube at the origin
    vertices = [
        [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
        [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
    ]
    
    # Shift the cube to the given position
    vertices = [[x + position[0], y + position[1], z + position[2]] for x, y, z in vertices]
    
    # Define the 6 faces of the cube
    faces = [
        [vertices[j] for j in [0, 1, 2, 3]],
        [vertices[j] for j in [4, 5, 6, 7]], 
        [vertices[j] for j in [0, 1, 5, 4]], 
        [vertices[j] for j in [2, 3, 7, 6]], 
        [vertices[j] for j in [1, 2, 6, 5]],
        [vertices[j] for j in [4, 7, 3, 0]]
    ]
    
    ax.add_collection3d(Poly3DCollection(faces, facecolors='lightgrey', linewidths=1, edgecolors='black', alpha=1))

def plot_shape(elev=20, azim=30, traj=None, name = "test2.jpg"):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    cube_positions = []
    x_max =0 
    y_max =0 
    z_max =0 
    for i in range(len(traj)-1):
        p = traj[i]
        x_max = max(x_max, p[0])
        y_max = max(y_max, p[1])
        z_max = max(z_max, p[2])
        p_next = traj[i+1]
        #print(p, p_next)
        if p[0] != p_next[0]:
            #print("0")
            for j in range(p[0],p_next[0], 1 if p[0]<p_next[0] else -1):
                cube_positions.append((j,p[1],p[2]))
        elif p[1] != p_next[1]:
            #print("1")
            for j in range(p[1],p_next[1], 1 if p[1]<p_next[1] else -1):
                cube_positions.append((p[0],j,p[2]))
        elif p[2] != p_next[2]:
            #print("2")
            for j in range(p[2],p_next[2], 1 if p[2]<p_next[2] else -1):
                cube_positions.append((p[0],p[1],j))
    cube_positions.append(traj[-1])
    x_max = max(x_max, traj[-1][0])
    y_max = max(y_max, traj[-1][1])
    z_max = max(z_max, traj[-1][2])
    # print(cube_positions)
    # print(x_max,y_max,z_max)
    
    # breakpoint()
    # Draw each cube
    for position in cube_positions:
        draw_cube(ax, position)
    
    ax.set_box_aspect([7, 6, 7])
    # Set the limits
    max_xyz = max(x_max, y_max, z_max)
    ax.set_xlim([0, max_xyz+2])
    ax.set_ylim([0, max_xyz+2])
    ax.set_zlim([0, max_xyz+2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # Remove axes
    ax.axis('off')
    
    # Set elevation and azimuth
    ax.view_init(elev=elev, azim=azim)

    plt.show()
    if os.path.dirname(name) and not os.path.exists(os.path.dirname(name)):
        # breakpoint()
        os.makedirs(os.path.dirname(name))
    plt.savefig(name)
    plt.close()

import numpy as np
from copy import deepcopy
import json, tqdm


def is_same_traj(traj1, traj2):
    def traverse(traj):
        path = []
        for idx in range(len(traj)-1):
            vec = traj[idx + 1] - traj[idx]
            assert np.bool_(vec).sum() == 1, f"should only 1 element is different from 0 in vec, vec: {vec}"
            path.append(abs(vec[np.nonzero(vec)[0][0]]))
            
        vec1 = traj[1] - traj[0] # actual the x axis
        vec2 = traj[2] - traj[1] # actual the y axis
        z = np.cross(vec1, vec2) / np.linalg.norm(np.cross(vec1, vec2)) # actual the z axis
        vec3 = traj[3] - traj[2] 
        d = np.dot(vec3, z)
        if d > 0:
            path.extend(["+x", "+y", "+z", "+x"])
        elif d < 0:
            path.extend(["+x", "+y", "-z", "+x"])
        else:
            raise ValueError(f"d should be either greater than 0 or less than 0, but it is {d}")
        
        return path
    
    path1 = traverse(traj1)
    path2 = traverse(traj2)
    path2_reversed = traverse(list(reversed(traj2)))
    # print(f"path1: {path1}, path2: {path2}, path2_reversed: {path2_reversed}")
    return path1 == path2 or path1 == path2_reversed
    

import random
def tarjs_from_ls(l, choice = None, max_xyz=7):
    
    # item in l should be greater than or equal to 2
    assert all([item >= 2 for item in l]), f"all items in l should be greater than or equal to 2, l: {l}"
    # boundary check
    assert l[0] + l[3] <= max_xyz, f"l[0] + l[3] should be less than or equal to {max_xyz}, but it is {l[0] + l[3]}"
    assert l[1] <= max_xyz, f"l[1] should be less than or equal to {max_xyz}, but it is {l[1]}"
    assert l[2] <= max_xyz, f"l[2] should be less than or equal to {max_xyz}, but it is {l[2]}"
    
    choice_candidates = [
        ["+x", "+y", "+z", "+x"],
        ["+x", "+y", "-z", "+x"],
        ["+x", "-y", "+z", "+x"],
        ["+x", "-y", "-z", "+x"],
        ["+x", "+z", "+y", "+x"],
        ["+x", "+z", "-y", "+x"],
        ["+x", "-z", "+y", "+x"],
        ["+x", "-z", "-y", "+x"],
        ["-x", "+y", "+z", "-x"],
        ["-x", "+y", "-z", "-x"],
        ["-x", "-y", "+z", "-x"],
        ["-x", "-y", "-z", "-x"],
        ["-x", "+z", "+y", "-x"],
        ["-x", "+z", "-y", "-x"],
        ["-x", "-z", "+y", "-x"],
        ["-x", "-z", "-y", "-x"],
        ["+y", "+x", "+z", "+y"],
        ["+y", "+x", "-z", "+y"],
        ["+y", "-x", "+z", "+y"],
        ["+y", "-x", "-z", "+y"],
        ["+y", "+z", "+x", "+y"],
        ["+y", "+z", "-x", "+y"],
        ["+y", "-z", "+x", "+y"],
        ["+y", "-z", "-x", "+y"],
        ["-y", "+x", "+z", "-y"],
        ["-y", "+x", "-z", "-y"],
        ["-y", "-x", "+z", "-y"],
        ["-y", "-x", "-z", "-y"],
        ["-y", "+z", "+x", "-y"],
        ["-y", "+z", "-x", "-y"],
        ["-y", "-z", "+x", "-y"],
        ["-y", "-z", "-x", "-y"],
        ["+z", "+x", "+y", "+z"],
        ["+z", "+x", "-y", "+z"],
        ["+z", "-x", "+y", "+z"],
        ["+z", "-x", "-y", "+z"],
        ["+z", "+y", "+x", "+z"],
        ["+z", "+y", "-x", "+z"],
        ["+z", "-y", "+x", "+z"],
        ["+z", "-y", "-x", "+z"],
        ["-z", "+x", "+y", "-z"],
        ["-z", "+x", "-y", "-z"],
        ["-z", "-x", "+y", "-z"],
        ["-z", "-x", "-y", "-z"],
        ["-z", "+y", "+x", "-z"],
        ["-z", "+y", "-x", "-z"],
        ["-z", "-y", "+x", "-z"],
        ["-z", "-y", "-x", "-z"],
    ]
    if choice == None or choice not in choice_candidates:
        choice = random.choice(choice_candidates)
    
    add_sub_dict = {"+": 1, "-": -1}
    xyz_idx_dict = {"x": 0, "y": 1, "z": 2}
    start_pos = [-1, -1, -1]
    if choice[0][0] == "+":
        start_pos[xyz_idx_dict[choice[0][1]]] = 0
    elif choice[0][0] == "-":
        start_pos[xyz_idx_dict[choice[0][1]]] = l[0] - 1 + l[3] - 1
    else:
        raise ValueError(f"choice[0][0] should be either '+' or '-'")
    
    if choice[1][0] == "+":
        start_pos[xyz_idx_dict[choice[1][1]]] = 0
    elif choice[1][0] == "-":
        start_pos[xyz_idx_dict[choice[1][1]]] = l[1] - 1
    else:
        raise ValueError(f"choice[1][0] should be either '+' or '-'")
    
    if choice[2][0] == "+":
        start_pos[xyz_idx_dict[choice[2][1]]] = 0
    elif choice[2][0] == "-":
        start_pos[xyz_idx_dict[choice[2][1]]] = l[2] - 1
    else:
        raise ValueError(f"choice[2][0] should be either '+' or '-'")
    
    assert start_pos[0] != -1 and start_pos[1] != -1 and start_pos[2] != -1, f"start_pos: {start_pos}"
    
    traj = [start_pos]
    for idx, path in enumerate(choice):
        pos = deepcopy(traj[-1])
        pos[xyz_idx_dict[path[1]]] += add_sub_dict[path[0]] * (l[idx] - 1)
        traj.append(deepcopy(pos))
        
    # print(f"choice: {choice} traj: {traj}")
    return traj

def all_adds(total):
    a = []
    for i in range(2, total+1):
        for j in range(2, total+1):
            for k in range(2, total+1):
                for l in range(2, total+1):
                    if i+j+k+l == total:
                        a.append((i, j, k, l))
    
    return set(a)

def all_trajs_from_ls(l, max_xyz):
    
    # item in l should be greater than or equal to 2
    try:
        assert all([item >= 2 for item in l]), f"all items in l should be greater than or equal to 2, l: {l}"
        # boundary check
        assert l[0] + l[3] <= max_xyz, f"l[0] + l[3] should be less than or equal to {max_xyz}, but it is {l[0] + l[3]}"
        assert l[1] <= max_xyz, f"l[1] should be less than or equal to {max_xyz}, but it is {l[1]}"
        assert l[2] <= max_xyz, f"l[2] should be less than or equal to {max_xyz}, but it is {l[2]}"
    except Exception as e:
        # print(e)
        return [], []
    
    choice_candidates = [
        ["+x", "+y", "+z", "+x"],
        ["+x", "+y", "-z", "+x"],
        ["+x", "-y", "+z", "+x"],
        ["+x", "-y", "-z", "+x"],
        ["+x", "+z", "+y", "+x"],
        ["+x", "+z", "-y", "+x"],
        ["+x", "-z", "+y", "+x"],
        ["+x", "-z", "-y", "+x"],
        ["-x", "+y", "+z", "-x"],
        ["-x", "+y", "-z", "-x"],
        ["-x", "-y", "+z", "-x"],
        ["-x", "-y", "-z", "-x"],
        ["-x", "+z", "+y", "-x"],
        ["-x", "+z", "-y", "-x"],
        ["-x", "-z", "+y", "-x"],
        ["-x", "-z", "-y", "-x"],
        ["+y", "+x", "+z", "+y"],
        ["+y", "+x", "-z", "+y"],
        ["+y", "-x", "+z", "+y"],
        ["+y", "-x", "-z", "+y"],
        ["+y", "+z", "+x", "+y"],
        ["+y", "+z", "-x", "+y"],
        ["+y", "-z", "+x", "+y"],
        ["+y", "-z", "-x", "+y"],
        ["-y", "+x", "+z", "-y"],
        ["-y", "+x", "-z", "-y"],
        ["-y", "-x", "+z", "-y"],
        ["-y", "-x", "-z", "-y"],
        ["-y", "+z", "+x", "-y"],
        ["-y", "+z", "-x", "-y"],
        ["-y", "-z", "+x", "-y"],
        ["-y", "-z", "-x", "-y"],
        ["+z", "+x", "+y", "+z"],
        ["+z", "+x", "-y", "+z"],
        ["+z", "-x", "+y", "+z"],
        ["+z", "-x", "-y", "+z"],
        ["+z", "+y", "+x", "+z"],
        ["+z", "+y", "-x", "+z"],
        ["+z", "-y", "+x", "+z"],
        ["+z", "-y", "-x", "+z"],
        ["-z", "+x", "+y", "-z"],
        ["-z", "+x", "-y", "-z"],
        ["-z", "-x", "+y", "-z"],
        ["-z", "-x", "-y", "-z"],
        ["-z", "+y", "+x", "-z"],
        ["-z", "+y", "-x", "-z"],
        ["-z", "-y", "+x", "-z"],
        ["-z", "-y", "-x", "-z"],
    ]
    trajs_1 = []
    trajs_2 = []
    traj_reference = tarjs_from_ls(l, choice=choice_candidates[0])
    
    for idx, choice in enumerate(choice_candidates):
        traj = tarjs_from_ls(l, choice=choice)
        if is_same_traj(np.array(traj_reference), np.array(traj)):
            trajs_1.append(deepcopy(traj))
        else:
            trajs_2.append(deepcopy(traj))
    return trajs_1, trajs_2


import itertools

angles = [45, 135, 225, 315]
# angles = [30, 60, 120, 150, 210, 240, 300, 330]
number_of_blocks = 15 # actual number of blocks = number_of_blocks - 3. Because the blocks at the three corners overlap, they are repeatedly calculated 3 times
adds = all_adds(number_of_blocks)

print(len(adds))
datas = []
for a in adds:
    trajs_1, trajs_2 = all_trajs_from_ls(a, max_xyz=7)
    if len(trajs_1) == 0 or len(trajs_2) == 0:
        continue
    
    trajs_1_com = list(itertools.combinations(trajs_1, 2))
    for item in trajs_1_com:
        ori = {
            "traj": item[0],
            "elev": 45,
            "azim": 45
        }
        right_ = {
            "traj": item[1],
            "elev": 45,
            "azim": 45
        }
        wrongs = random.sample(trajs_2, 3)
        wrong_1 = {
            "traj": wrongs[0],
            "elev": 45,
            "azim": 45
        }
        wrong_2 = {
            "traj": wrongs[1],
            "elev": 45,
            "azim": 45
        }
        wrong_3 = {
            "traj": wrongs[2],
            "elev": 45,
            "azim": 45
        }
        datas.append({
            "ori": deepcopy(ori),
            "right": deepcopy(right_),
            "wrong_1": deepcopy(wrong_1),
            "wrong_2": deepcopy(wrong_2),
            "wrong_3": deepcopy(wrong_3)
        })
        
    trajs_2_com = list(itertools.combinations(trajs_2, 2))
    for item in trajs_2_com:
        ori = {
            "traj": item[0],
            "elev": 45,
            "azim": 45
        }
        right_ = {
            "traj": item[1],
            "elev": 45,
            "azim": 45
        }
        wrongs = random.sample(trajs_1, 3)
        wrong_1 = {
            "traj": wrongs[0],
            "elev": 45,
            "azim": 45
        }
        wrong_2 = {
            "traj": wrongs[1],
            "elev": 45,
            "azim": 45
        }
        wrong_3 = {
            "traj": wrongs[2],
            "elev": 45,
            "azim": 45
        }
        datas.append({
            "ori": deepcopy(ori),
            "right": deepcopy(right_),
            "wrong_1": deepcopy(wrong_1),
            "wrong_2": deepcopy(wrong_2),
            "wrong_3": deepcopy(wrong_3)
        })      

print(f"size of datas: {len(datas)}")
# breakpoint()
mrt_png_data_path = "/nfs_global/S/tianzikang/project_data/spatial_intelligence/mrt_data/"
# remove the existing data
os.system(f"rm -rf {mrt_png_data_path}")
os.makedirs(mrt_png_data_path, exist_ok=True)
np.random.shuffle(datas)
for idx, item in tqdm.tqdm(enumerate(datas)):
    # if idx >= 100:
    #     break
    ori = item["ori"]
    right = item["right"]
    wrong_1 = item["wrong_1"]
    wrong_2 = item["wrong_2"]
    wrong_3 = item["wrong_3"]
    right_choice = np.random.choice(["A", "B", "C", "D"])
    wrong_choices = ["A", "B", "C", "D"]
    wrong_choices.remove(right_choice)
    np.random.shuffle(wrong_choices)
    os.makedirs(f"{mrt_png_data_path}/{idx}", exist_ok=True)
    plot_shape(elev=ori["elev"], azim=ori["azim"], traj=ori["traj"], name=f"{mrt_png_data_path}/{idx}/ori.png")
    plot_shape(elev=right["elev"], azim=right["azim"], traj=right["traj"], name=f"{mrt_png_data_path}/{idx}/{right_choice}.png")
    plot_shape(elev=wrong_1["elev"], azim=wrong_1["azim"], traj=wrong_1["traj"], name=f"{mrt_png_data_path}/{idx}/{wrong_choices[0]}.png")
    plot_shape(elev=wrong_2["elev"], azim=wrong_2["azim"], traj=wrong_2["traj"], name=f"{mrt_png_data_path}/{idx}/{wrong_choices[1]}.png")
    plot_shape(elev=wrong_3["elev"], azim=wrong_3["azim"], traj=wrong_3["traj"], name=f"{mrt_png_data_path}/{idx}/{wrong_choices[2]}.png")
    with open(f"{mrt_png_data_path}/{idx}/answer.json", "w") as f:
        json.dump({"answer": right_choice}, f)
    

generate_huggingface_datasets = True
if not generate_huggingface_datasets:
    exit()
    
import datasets
datasets.builder.has_sufficient_disk_space = lambda needed_bytes, directory='.': True

from datasets import load_dataset, Dataset
from PIL import Image

prompt = """
Here is an image of a three-dimensional shape.
<IMAGE OF REFERENCE 3D SHAPE>

Which of these images show the same object rotated in 3D?

A. <CHOICE 1 IMAGE>

B. <CHOICE 2 IMAGE>

C. <CHOICE 3 IMAGE>

D. <CHOICE 4 IMAGE>

Think step by step. Your response should include reasoning process and answer. Reasoning process and answer are enclosed whthin <think> </think> and <answer> </answer> tags respectively, i.e., <think> reasoning process here </think>. <answer> answer here </answer>.
"""

def make_role_prompt():
    prompt = [
        {
            "role": "user", 
            "content": [
                {
                    "type": "text",
                    "text": "Here is an image of a three-dimensional shape.\n"
                },
                {
                    "type": "image",
                    "text": None
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
                    "type": "image",
                    "text": None
                },
                {
                    "type": "text",
                    "text": "\nB.\n"
                },
                {
                    "type": "image",
                    "text": None
                },
                {
                    "type": "text",
                    "text": "\nC.\n"
                },
                {
                    "type": "image",
                    "text": None
                },
                {
                    "type": "text",
                    "text": "\nD.\n"
                },
                {
                    "type": "image",
                    "text": None
                },
                {
                    "type": "text",
                    "text": "\nThink step by step. Your response should include reasoning process and answer. Reasoning process and answer are enclosed whthin <think> </think> and <answer> </answer> tags respectively, i.e., <think> reasoning process here </think>. <answer> answer here </answer>."
                }
            ]
        }
    ]
    
    return prompt

ori = []
a_s = []
b_s = []
c_s = []
d_s = []
problem = []
solution = []
for d in tqdm.tqdm(os.listdir(mrt_png_data_path)):
    if os.path.isdir(f"{mrt_png_data_path}/{d}"):
        problem.append(make_role_prompt())
        with open(f"{mrt_png_data_path}/{d}/answer.json", "r") as f:
            answer = json.load(f)["answer"]
            solution.append(f"<think>...</think>\n<answer>{answer}</answer>")
            with Image.open(f"{mrt_png_data_path}/{d}/ori.png") as img:
                ori.append(img)
            with Image.open(f"{mrt_png_data_path}/{d}/A.png") as img:
                a_s.append(img)
            with Image.open(f"{mrt_png_data_path}/{d}/B.png") as img:
                b_s.append(img)
            with Image.open(f"{mrt_png_data_path}/{d}/C.png") as img:
                c_s.append(img)
            with Image.open(f"{mrt_png_data_path}/{d}/D.png") as img:
                d_s.append(img)


ds = Dataset.from_dict(
    {
        "ori": ori,
        "A": a_s,
        "B": b_s,
        "C": c_s,
        "D": d_s,
        "prompt": problem,
        "solution": solution
    }
)

save_path = f"./mrt_data_ds/train/train/"
if os.path.exists(save_path):
    os.system(f"rm -rf {save_path}")
ds.save_to_disk(save_path)

dataset_dict_path = f"./mrt_data_ds/train/dataset_dict.json"
json_obs = {"splits": ["train"]}
with open(dataset_dict_path, "w") as f:
    json.dump(json_obs, f)
    
print("Done!")
    
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

# # reference
# plot_shape(elev=30, azim=30, traj = [(3,5,0),
#                                      (3,3,0),
#                                      (0,3,0),
#                                      (0,3,3),
#                                      (0,0,3)], name='reference.jpg')
# angles = [30,60,120,150,210,240,300,330]
# for elev in angles:
#     for azim in angles:
#         plot_shape(elev=elev, azim=azim, traj = [(3,5,0),
#                                      (3,3,0),
#                                      (0,3,0),
#                                      (0,3,3),
#                                      (0,0,3)], name='refs/'+str(elev)+'_'+str(azim)+'.jpg')
# # c1 wrong
# # plot_shape(elev=240, azim=30, traj = [(3,0,0),
# #                                      (3,2,0),
# #                                      (0,2,0),
# #                                      (0,2,3),
# #                                      (0,5,3)], name='c1.jpg')

# plot_shape(elev=30, azim=30, traj = [(3,0,0),
#                                      (3,2,0),
#                                      (0,2,0),
#                                      (0,2,3),
#                                      (0,5,3)], name='c1.jpg')

# # c2 right
# plot_shape(elev=225, azim=45, traj = [(3,5,0),
#                                      (3,3,0),
#                                      (0,3,0),
#                                      (0,3,3),
#                                      (0,0,3)], name='c2.jpg')
# # c3 wrong
# plot_shape(elev=30, azim=70, traj = [(3,0,0),
#                                      (3,2,0),
#                                      (0,2,0),
#                                      (0,2,3),
#                                      (0,5,3)], name='c3.jpg')
# # c4 wrong
# plot_shape(elev=30, azim=80, traj = [(3,0,0),
#                                      (3,2,0),
#                                      (0,2,0),
#                                      (0,2,3),
#                                      (0,5,3)], name='c4.jpg')
# for elev in angles:
#     for azim in angles:
#         plot_shape(elev=elev, azim=azim, traj = [(3,0,0),
#                                      (3,2,0),
#                                      (0,2,0),
#                                      (0,2,3),
#                                      (0,5,3)], name='opts/'+str(elev)+'_'+str(azim)+'.jpg')
        

import numpy as np
from copy import deepcopy
import json, tqdm
# def random_shape():
#     lengths = [
#         [3, 3, 3, 3],
#         [2, 3, 3, 4],
#         [2, 2, 4, 4],
#         [2, 2, 3, 5],
#         # [4, 4, 4, 4]
#     ]
    
#     for l in lengths:
#         np.random.shuffle(l)
#         pos1 = (l[1], l[0] + l[3] - 1, 0)
#         pos2 = (l[1], l[3], 0)
#         pos3 = (0, l[3], 0)
#         pos4 = (0, l[3], l[2])
#         pos5 = (0, 0, l[2])
#         traj = [pos1, pos2, pos3, pos4, pos5]
        
#         plot_shape(elev=30, azim=30, traj=traj, name='random_shapes/'+"_".join([str(item) for item in l])+'.png')


def is_same_traj(traj1, traj2):
    delta_traj1 = [(traj1[i+1][0]-traj1[i][0], traj1[i+1][1]-traj1[i][1], traj1[i+1][2]-traj1[i][2]) for i in range(len(traj1)-1)]
    delta_traj2 = [(traj2[i+1][0]-traj2[i][0], traj2[i+1][1]-traj2[i][1], traj2[i+1][2]-traj2[i][2]) for i in range(len(traj2)-1)]
    reverse_traj2 = [traj2[i] for i in range(len(traj2)-1, -1, -1)]
    delta_reverse_traj2 = [(reverse_traj2[i+1][0]-reverse_traj2[i][0], reverse_traj2[i+1][1]-reverse_traj2[i][1], reverse_traj2[i+1][2]-reverse_traj2[i][2]) for i in range(len(reverse_traj2)-1)]
    transpose_delta_reverse_traj2 = []
    for item in delta_reverse_traj2:
        if item[0] != 0:
            transpose_delta_reverse_traj2.append((item[2], item[1], item[0]))
        elif item[1] != 0:
            transpose_delta_reverse_traj2.append((item[0], -item[1], item[2]))
        elif item[2] != 0:
            transpose_delta_reverse_traj2.append((item[2], item[1], item[0]))
            
    
    return delta_traj1 == delta_traj2 or delta_traj1 == transpose_delta_reverse_traj2

def tarjs_from_ls(l, choice = None):
    # 0 is prime, 1 is mirror image
    if choice == None or choice not in [0, 1]:
        choice = np.random.choice([0, 1])
    if choice == 0:
        l_copy = [l[0], l[1] - 1, l[2] - 1, l[3] - 1]
        pos1 = (l_copy[1], l_copy[0] + l_copy[3] - 1, 0)
        pos2 = (l_copy[1], l_copy[3], 0)
        pos3 = (0, l_copy[3], 0)
        pos4 = (0, l_copy[3], l_copy[2])
        pos5 = (0, 0, l_copy[2])
        traj = [pos1, pos2, pos3, pos4, pos5]
        return traj
    elif choice == 1:
        l_copy = [l[0], l[1] - 1, l[2] - 1, l[3] - 1]
        pos1 = (l_copy[1], 0, 0)
        pos2 = (l_copy[1], l_copy[0] - 1, 0)
        pos3 = (0, l_copy[0] - 1, 0)
        pos4 = (0, l_copy[0] - 1, l_copy[2])
        pos5 = (0, l_copy[0] + l_copy[3] - 1, l_copy[2])
        traj = [pos1, pos2, pos3, pos4, pos5]
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


# l1 = [2, 4, 4, 5]
# l1 = [2, 2, 3, 5]
# l2 = [5, 4, 4, 2]

# traj1 = tarjs_from_ls(l1, choice=0)
# traj2 = tarjs_from_ls(l1, choice=1)
# print(is_same_traj(traj1, traj2))

# plot_shape(elev=30, azim=30, traj=traj1, name='traj1.png')
# # plot_shape(elev=30, azim=30, traj=traj2, name='traj2.png')
# plot_shape(elev=225, azim=30, traj=traj1, name="traj2.png")

import itertools
# l1_perm = list(itertools.permutations(l1))
# l1_perm_set = set(l1_perm)

# print(f"len of l1_perm: {len(l1_perm)}")
# print(f"len of l1_perm_set: {len(l1_perm_set)}")
# for p in l1_perm:
#     print(f"perm: {p}")


angles = [30, 60, 120, 150, 210, 240, 300, 330]
right_candidates_num = 3
total = 15 # actual number of blocks = total - 3. See trajs_from_ls can understand this relation
adds = all_adds(total)
# print(f"adds: {adds}")

datas = []
for a in adds:
    data = {}
    original_traj = tarjs_from_ls(a, choice=0)
    data["ori"] = {
        "traj": original_traj,
        "elev": 30,
        "azim": 30
    }
    data["right"] = []
    angles_cp = deepcopy(angles)
    angles_cp.remove(30)
    # elevs_candidates = np.random.choice(angles_cp, size=right_candidates_num, replace=False)
    elevs_candidates = np.random.choice([150, 210, 240, 300, 330], size=right_candidates_num, replace=False)
    for elev in elevs_candidates:
        data["right"].append(
            {
                "traj": original_traj,
                "elev": elev,
                "azim": 30
                # "elev": 30,
                # "azim": elev
            }
        )
    data["wrong"] = []
    mirrored_traj = tarjs_from_ls(a, choice=1)
    if not is_same_traj(original_traj, mirrored_traj):
        data["wrong"].append(
                {
                    "traj": mirrored_traj,
                    "elev": 30,
                    "azim": 30
                }
            )
        for elev in elevs_candidates:
            data["wrong"].append(
                {
                    "traj": mirrored_traj,
                    "elev": elev,
                    "azim": 30
                    # "elev": 30,
                    # "azim": elev
                }
            )
    a_perm_set = set(itertools.permutations(a))
    for a_perm in a_perm_set:
        a_perm_original_traj = tarjs_from_ls(a_perm, choice=0)
        a_perm_mirrored_traj = tarjs_from_ls(a_perm, choice=1)
        if not is_same_traj(original_traj, a_perm_original_traj):
            for elev in elevs_candidates:
                data["wrong"].append(
                    {
                        "traj": a_perm_original_traj,
                        "elev": elev,
                        "azim": 30
                        # "elev": 30,
                        # "azim": elev
                    }
                )
        if not is_same_traj(mirrored_traj, a_perm_mirrored_traj):
            for elev in elevs_candidates:
                data["wrong"].append(
                    {
                        "traj": a_perm_mirrored_traj,
                        "elev": elev,
                        "azim": 30
                        # "elev": 30,
                        # "azim": elev
                    }
                )
    # datas.append(data)
    np.random.shuffle(data["wrong"])
    actual_data = {}
    actual_data["ori"] = data["ori"]
    for right in data["right"]:
        actual_data["right"] = right
        for idx in range(0, len(data["wrong"]), 3):
            if idx + 2 >= len(data["wrong"]):
                break
            actual_data["wrong_1"] = data["wrong"][idx]
            actual_data["wrong_2"] = data["wrong"][idx+1]
            actual_data["wrong_3"] = data["wrong"][idx+2]
            datas.append(deepcopy(actual_data))
            
# print(f"len of datas: {len(datas)}")

os.makedirs("mrt_data", exist_ok=True)
np.random.shuffle(datas)
for idx, item in tqdm.tqdm(enumerate(datas)):
    if idx >= 100:
        break
    ori = item["ori"]
    right = item["right"]
    wrong_1 = item["wrong_1"]
    wrong_2 = item["wrong_2"]
    wrong_3 = item["wrong_3"]
    right_choice = np.random.choice(["A", "B", "C", "D"])
    wrong_choices = ["A", "B", "C", "D"]
    wrong_choices.remove(right_choice)
    np.random.shuffle(wrong_choices)
    os.makedirs(f"mrt_data/{idx}", exist_ok=True)
    plot_shape(elev=ori["elev"], azim=ori["azim"], traj=ori["traj"], name=f"mrt_data/{idx}/ori.png")
    plot_shape(elev=right["elev"], azim=right["azim"], traj=right["traj"], name=f"mrt_data/{idx}/{right_choice}.png")
    plot_shape(elev=wrong_1["elev"], azim=wrong_1["azim"], traj=wrong_1["traj"], name=f"mrt_data/{idx}/{wrong_choices[0]}.png")
    plot_shape(elev=wrong_2["elev"], azim=wrong_2["azim"], traj=wrong_2["traj"], name=f"mrt_data/{idx}/{wrong_choices[1]}.png")
    plot_shape(elev=wrong_3["elev"], azim=wrong_3["azim"], traj=wrong_3["traj"], name=f"mrt_data/{idx}/{wrong_choices[2]}.png")
    with open(f"mrt_data/{idx}/answer.json", "w") as f:
        json.dump({"answer": right_choice}, f)
    
# print("done")

generate_huggingface_datasets = False
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
for d in tqdm.tqdm(os.listdir("./mrt_data")):
    if os.path.isdir(f"./mrt_data/{d}"):
        problem.append(make_role_prompt())
        with open(f"./mrt_data/{d}/answer.json", "r") as f:
            answer = json.load(f)["answer"]
            solution.append(f"<think>...</think>\n<answer>{answer}</answer>")
            with Image.open(f"./mrt_data/{d}/ori.png") as img:
                ori.append(img)
            with Image.open(f"./mrt_data/{d}/A.png") as img:
                a_s.append(img)
            with Image.open(f"./mrt_data/{d}/B.png") as img:
                b_s.append(img)
            with Image.open(f"./mrt_data/{d}/C.png") as img:
                c_s.append(img)
            with Image.open(f"./mrt_data/{d}/D.png") as img:
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

# os.system(f"rm -rf ./mrt_data")
    
import base64

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def flatten(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):  # 检查元素是否可以迭代
            flat_list.extend(flatten(item))  # 如果是列表，递归调用flatten函数
        else:
            flat_list.append(item)  # 如果不是列表，直接添加到结果列表中
    return flat_list

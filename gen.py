import os
import json

# 指定要扫描的目录
root_directory = '.'

# 扫描除 'data' 之外的所有目录
subdirectories = [d for d in os.listdir(root_directory) if os.path.isdir(os.path.join(root_directory, d)) and d != 'data']

# 确保 'data' 目录存在
data_directory = os.path.join(root_directory, 'data')
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

# 对于每个目录，生成对应的 JSON 文件并将其存放在 'data' 目录下
for subdir in subdirectories:
    subdir_path = os.path.join(root_directory, subdir)
    png_files = [f for f in os.listdir(subdir_path) if f.endswith('.png') and not f.endswith('thumb.png')]

    # 生成 JSON 文件内容
    json_data = {
        'images': png_files
    }

    # 将 JSON 数据写入文件
    json_file_path = os.path.join(data_directory, f'{subdir}.json')
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

# 生成 data.json 文件
data_json_data = {
    'characters': subdirectories
}

data_json_file_path = os.path.join(data_directory, 'data.json')
with open(data_json_file_path, 'w') as data_json_file:
    json.dump(data_json_data, data_json_file, indent=4)

print("JSON files generated successfully.")


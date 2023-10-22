import os
import sys
import json
import argparse
import zipfile
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from pathlib import Path

def encrypt_file(file_path, output_path, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)

    with open(file_path, 'rb') as file:
        data = file.read()

    encrypted_data = cipher.encrypt(pad(data, AES.block_size))

    with open(output_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

def create_thumbnail(image_path, output_path, max_size=400):
    with Image.open(image_path) as img:
        width, height = img.size
        aspect_ratio = float(width) / float(height)

        if width > height:
            new_width = max_size
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = max_size
            new_width = int(new_height * aspect_ratio)

        img.thumbnail((new_width, new_height))
        img.save(output_path)

def create_image_list_json(directory, output_directory):
    image_list = []

    for file_name in os.listdir(directory):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_list.append(file_name)

    image_list_json = {"images": image_list}

    json_file_name = f"{Path(directory).name}.json"
    json_file_path = os.path.join(output_directory, json_file_name)

    with open(json_file_path, 'w') as json_file:
        json.dump(image_list_json, json_file)

def create_character_list_json(root_directory, output_directory):
    character_list = []

    for subdir in os.listdir(root_directory):
        subdir_path = os.path.join(root_directory, subdir)
        if os.path.isdir(subdir_path):
            character_list.append(subdir)

    character_list_json = {"characters": character_list}

    json_file_path = os.path.join(output_directory, "data.json")

    with open(json_file_path, 'w') as json_file:
        json.dump(character_list_json, json_file)

def process_images_in_directory(directory, output_directory, key, iv, force=False):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    print(f"Processing images in directory: {directory}")

    for file_name in os.listdir(directory):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_path = os.path.join(directory, file_name)
            encrypted_file_path = os.path.join(output_directory, file_name)
            thumbnail_file_path = os.path.join(output_directory, Path(file_name).stem + '_thumb.png')

            if not force and os.path.exists(encrypted_file_path) and os.path.exists(thumbnail_file_path):
                print(f"  Skipping existing files for image: {file_name}")
            else:
                print(f"  Encrypting image: {file_name}")
                encrypt_file(file_path, encrypted_file_path, key, iv)

                print(f"  Creating thumbnail: {file_name}")
                create_thumbnail(file_path, thumbnail_file_path)

def process_images_in_subdirectories(root_directory, output_root_directory, key, iv, force=False):
    data_directory = os.path.join(output_root_directory, "data")
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    print("Creating character list JSON file.")
    create_character_list_json(root_directory, data_directory)

    for subdir in os.listdir(root_directory):
        subdir_path = os.path.join(root_directory, subdir)
        if os.path.isdir(subdir_path):
            output_subdir_path = os.path.join(output_root_directory, subdir)
            process_images_in_directory(subdir_path, output_subdir_path, key, iv, force)
            print(f"Creating image list JSON file for directory: {subdir}")
            create_image_list_json(subdir_path, data_directory)

def read_key_and_iv(file_path):
    with open(file_path, 'rb') as file:
        key = file.readline().strip()
        iv = file.readline().strip()
    return key, iv

def zip_data_directory(output_root_directory):
    data_directory = os.path.join(output_root_directory, "data")
    zip_file_path = os.path.join(output_root_directory, "data.zip")

    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, _, files in os.walk(data_directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_root_directory)
                zip_file.write(file_path, arcname)

    print(f"Created data.zip in directory: {output_root_directory}")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Encrypt images and generate thumbnails.")
    parser.add_argument('--force', action='store_true', help="Force full generation, even if files already exist.")
    args = parser.parse_args()

    root_directory = "./I/"
    output_root_directory = "../MW2/I"

    # 使用相同的密钥和 IV 作为客户端应用程序
    key = b'D\x82,7\xba\x9f\x1e*\x92\xacM$\xe6>\xf2\xd0'
    iv = b'E\xda\x9c\x99?\\~\xa0e\x9a:\xdd\xaf\xc7\xb4@'

    print("Starting encryption, thumbnail generation, and JSON file creation.")
    process_images_in_subdirectories(root_directory, output_root_directory, key, iv, args.force)
    zip_data_directory(output_root_directory)

    print("Encryption, thumbnail generation, and JSON file creation complete.")

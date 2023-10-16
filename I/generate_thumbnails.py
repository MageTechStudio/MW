import os
import sys
from pathlib import Path
from PIL import Image

def generate_thumbnail(image_path, thumbnail_size=400, force=False):
    image = Image.open(image_path)
    thumb_filename = f"{image_path.stem}_thumb{image_path.suffix}"
    thumb_path = image_path.with_name(thumb_filename)

    if thumb_path.exists() and not force:
        print(f"Skipping existing thumbnail: {thumb_path}")
        return

    max_dimension = max(image.width, image.height)
    scale_factor = thumbnail_size / max_dimension
    new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
    thumbnail_image = image.resize(new_size, Image.ANTIALIAS)

    thumbnail_image.save(thumb_path)
    print(f"Generated thumbnail: {thumb_path}")

def process_directory(directory, force=False):
    for entry in os.scandir(directory):
        if entry.is_dir():
            process_directory(entry.path, force)
        elif entry.name.endswith(".png") and not entry.name.endswith("_thumb.png"):
            generate_thumbnail(Path(entry.path), force=force)

if __name__ == "__main__":
    root_directory = Path.cwd()
    force_generate = "--force" in sys.argv

    process_directory(root_directory, force=force_generate)

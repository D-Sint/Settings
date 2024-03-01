from PIL import Image
import os
from tqdm import tqdm
import argparse

def remove_metadata(directory):
    file_count = 0
    for root, _, files in os.walk(directory):
        file_count += len([filename for filename in files if filename.endswith((".jpg", ".jpeg", ".png"))])
    
    with tqdm(total=file_count) as pbar:
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith((".jpg", ".jpeg", ".png")):
                    filepath = os.path.join(root, filename)
                    try:
                        image = Image.open(filepath)
                        # Remove metadata
                        image_without_metadata = Image.new(image.mode, image.size)
                        image_without_metadata.putdata(list(image.getdata()))
                        image_without_metadata.save(filepath)
                        print(f"Metadata removed from {filename}")
                    except Exception as e:
                        print(f"Failed to process {filename}: {str(e)}")
                    pbar.update(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove metadata from images in a directory")
    parser.add_argument("directory", type=str, help="Path to the directory containing images")
    args = parser.parse_args()

    remove_metadata(args.directory)


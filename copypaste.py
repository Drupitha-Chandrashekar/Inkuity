import os
import shutil

# Set your source root directory containing multiple folders
source_root = 'C:\\Users\\ADMIN\\Downloads\\Abstract-Expressionism-20250602T092810Z-1-001'
# Set the target folder where all images will be copied
target_folder = 'D:\\faiss3\\artvee'  # e.g., './combined'

# Create target folder if it doesn't exist
os.makedirs(target_folder, exist_ok=True)

# Loop through each folder in the source root
for folder_name in os.listdir(source_root):
    folder_path = os.path.join(source_root, folder_name)

    # Skip if it's not a directory
    if not os.path.isdir(folder_path):
        continue

    # Loop through each file in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Skip if it's not a file
        if not os.path.isfile(file_path):
            continue

        # Build new filename
        new_file_name = f"{folder_name}_{file_name}"
        target_path = os.path.join(target_folder, new_file_name)

        # Copy the image to the target folder
        shutil.copy2(file_path, target_path)

print("✅ All images combined successfully.")

import os
import shutil

# Destination folder (existing)
folder_b = r'D:\faiss3\artvee'

# List of source folders
source_folders = [
    r'C:\Users\ADMIN\Downloads\dataset\wikiart\Early-Dynastic',
    r'C:\Users\ADMIN\Downloads\dataset\wikiart\Graffiti-Art',
    r'C:\Users\ADMIN\Downloads\dataset\wikiart\Sky-Art',
    r'C:\Users\ADMIN\Downloads\dataset\wikiart\Geometric'
]

for folder_c in source_folders:
    folder_c_name = os.path.basename(folder_c)

    for filename in os.listdir(folder_c):
        source_path = os.path.join(folder_c, filename)
        dest_path = os.path.join(folder_b, filename)

        # Check if file already exists in destination
        if os.path.exists(dest_path):
            # Prefix filename with folder name
            new_filename = f"{folder_c_name}_{filename}"
            dest_path = os.path.join(folder_b, new_filename)

        shutil.copy2(source_path, dest_path)

print("All images from source folders have been copied with duplicate handling.")
import os
import re
import shutil

# Directories
dir1 = 'D:\Temp\Slideshow\1'
dir2 = 'D:\Temp\Slideshow\2'
combined_dir = 'D:\Temp\Slideshow\EAST'

# Create combined directory if it doesn't exist
os.makedirs(combined_dir, exist_ok=True)

# Regex to extract leading number
pattern = re.compile(r'^(\d+)_')

# Track used numbers
used_numbers = set()
next_number = 1

def process_directory(source_dir):
    global next_number
    for filename in os.listdir(source_dir):
        match = pattern.match(filename)
        if match:
            while next_number in used_numbers:
                next_number += 1
            new_filename = f"{next_number}_{'_'.join(filename.split('_')[1:])}"
            src_path = os.path.join(source_dir, filename)
            dst_path = os.path.join(combined_dir, new_filename)
            shutil.copy2(src_path, dst_path)
            used_numbers.add(next_number)
            print(f"Copied and renamed: {filename} → {new_filename}")
            next_number += 1

# Process both directories
process_directory(dir1)
process_directory(dir2)import os
import re
import shutil

# Directories
dir1 = 'path/to/first_dir'
dir2 = 'path/to/second_dir'
combined_dir = 'path/to/combined_dir'

# Create combined directory if it doesn't exist
os.makedirs(combined_dir, exist_ok=True)

# Regex to extract leading number
pattern = re.compile(r'^(\d+)_')

# Track used numbers
used_numbers = set()
next_number = 1

def process_directory(source_dir):
    global next_number
    for filename in os.listdir(source_dir):
        match = pattern.match(filename)
        if match:
            while next_number in used_numbers:
                next_number += 1
            new_filename = f"{next_number}_{'_'.join(filename.split('_')[1:])}"
            src_path = os.path.join(source_dir, filename)
            dst_path = os.path.join(combined_dir, new_filename)
            shutil.copy2(src_path, dst_path)
            used_numbers.add(next_number)
            print(f"Copied and renamed: {filename} → {new_filename}")
            next_number += 1

# Process both directories
process_directory(dir1)
process_directory(dir2)
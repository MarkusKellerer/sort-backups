import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def remove_duplicates(duplicates_path):
    file_pattern = re.compile(r'^(.+?)(?:_\d{1,2})?(\.[^.]+)$')
    files_map = {}

    # Build a map of files without the counter suffix and their paths
    for filename in os.listdir(duplicates_path):
        match = file_pattern.match(filename)
        if match:
            base_filename, file_extension = match.groups()
            full_path = os.path.join(duplicates_path, filename)
            file_size = os.path.getsize(full_path)

            key = (base_filename, file_extension, file_size)
            print(key)
            if key not in files_map:
                files_map[key] = []
            files_map[key].append(full_path)

    # Remove duplicates: files with the same base name, extension, and size
    for (base_filename, file_extension, file_size), paths in files_map.items():
        if len(paths) > 1:
            paths.sort()  # Sort to keep the first file
            original_file = paths.pop(0)
            print(f"Keeping original file: {original_file}")
            for duplicate_file in paths:
                print(f"Removing duplicate file: {duplicate_file}")
                os.remove(duplicate_file)


def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        print(f"Looking for duplicate in selected folder: {folder_selected}")
        remove_duplicates(folder_selected)
        # Walk through the directory tree and call remove_duplicates on each subfolder
        for root, dirs, files in os.walk(folder_selected):
            dirs[:] = [d for d in dirs if os.path.join(root, d)]  # Exclude folders
            for dir in dirs:
                duplicates_path = os.path.join(root, dir)
                print(f"Looking for duplicate files in: {duplicates_path}")
                remove_duplicates(duplicates_path)
        messagebox.showinfo("Complete", "Duplicate removal complete.")

def exclude_folder():
    folder_to_exclude = filedialog.askdirectory(title="Select Folder to Exclude")
    if folder_to_exclude:
        excluded_folders_list.insert(tk.END, folder_to_exclude)

# Create the main window
root = tk.Tk()
root.title("Duplicate Remover")

# Create UI components
select_folder_button = tk.Button(root, text="Select Folder with Possible Duplicates", command=select_folder)
select_folder_button.pack()

# Run the application
root.mainloop()
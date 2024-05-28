import os
import shutil
import re
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox


def sort_images_by_date(base_path, destination_path, exclude_folders):
    date_pattern = re.compile(r'^(?:IMG[_-])?(\d{4})-?(\d{2})-?\d{2}[_ -].*\.(jpg|jpeg|png|gif|bmp|tiff|mp4)$', re.IGNORECASE)
    snapchat_pattern = re.compile(r'^Snapchat.*\.(jpg|jpeg|png|gif|bmp|tiff)$', re.IGNORECASE)
    fb_img_pattern = re.compile(r'^FB_IMG.*\.(jpg|jpeg|png|gif|bmp|tiff)$', re.IGNORECASE)

    snapchat_path = os.path.join(destination_path, "Snapchat")
    facebook_path = os.path.join(destination_path, "Facebook")
    unsorted_path = os.path.join(destination_path, "Unsorted")

    for dirpath, dirnames, filenames in os.walk(base_path):
        # Exclude specified folders
        dirnames[:] = [d for d in dirnames if os.path.join(dirpath, d) not in exclude_folders]

        for filename in filenames:
            src_file_path = os.path.join(dirpath, filename)
            if snapchat_pattern.match(filename):
                dest_folder = snapchat_path
            elif fb_img_pattern.match(filename):
                dest_folder = facebook_path
            else:
                match = date_pattern.match(filename)
                if match:
                    year, month = match.groups()[:2]
                    print(f'Read: {year} -> {month}')
                    year_path = os.path.join(destination_path, year)
                    month_path = os.path.join(year_path, month)
                    if not os.path.exists(month_path):
                        os.makedirs(month_path)
                    dest_folder = month_path
                else:
                    dest_folder = unsorted_path

            # Create the destination folder if it doesn't exist
            if not os.path.exists(dest_folder):
                 os.makedirs(dest_folder)

            dest_file_path = os.path.join(dest_folder, filename)

            # Ensure safety for files with the same name
            counter = 1
            file_root, file_ext = os.path.splitext(dest_file_path)
            while os.path.exists(dest_file_path):
                dest_file_path = f"{file_root}_{counter}{file_ext}"
                counter += 1

            shutil.move(src_file_path, dest_file_path)
            print(f'Moved: {src_file_path} -> {dest_file_path}')


def select_folder(path_var):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_var.set(folder_selected)


def exclude_folder():
    folder_to_exclude = filedialog.askdirectory(title="Select Folder to Exclude")
    if folder_to_exclude:
        excluded_folders_list.insert(tk.END, folder_to_exclude)
        excluded_folders.add(folder_to_exclude)

def delete_empty_folders(path):
    print("Starting to remove empty folders")
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):  # Walk the tree top-down
        if not dirnames and not filenames:  # Check if the folder is empty
            try:
                os.rmdir(dirpath)  # Attempt to remove the empty folder
                print(f"Removed empty folder: {dirpath}")
            except OSError as e:
                print(f"Error: {dirpath} : {e.strerror}")  # Print any error message


# Modify the start_sorting function to call delete_empty_folders after sorting
def start_sorting():
    source_folder = source_path.get()
    dest_folder = destination_path.get()
    if not source_folder or not dest_folder:
        messagebox.showerror("Error", "Please select both source and destination folders.")
        return

    exclude_folders = set(excluded_folders_list.get(0, tk.END))
    sort_images_by_date(source_folder, dest_folder, exclude_folders)

    delete_empty_folders(source_folder)

    messagebox.showinfo("Complete", "Sorting complete and empty folders removed.")

# Create the main window
root = tk.Tk()
root.title("Image Sorter")

# Store folder paths and excluded folders
source_path = tk.StringVar()
destination_path = tk.StringVar()
excluded_folders = set()

# Create UI components for source folder selection
source_folder_label = tk.Label(root, text="Source Folder:")
source_folder_label.pack()

source_folder_entry = tk.Entry(root, textvariable=source_path, width=50)
source_folder_entry.pack()

select_source_folder_button = tk.Button(root, text="Select Source Folder", command=lambda: select_folder(source_path))
select_source_folder_button.pack()

# Create UI components for destination folder selection
destination_folder_label = tk.Label(root, text="Destination Folder:")
destination_folder_label.pack()

destination_folder_entry = tk.Entry(root, textvariable=destination_path, width=50)
destination_folder_entry.pack()

select_destination_folder_button = tk.Button(root, text="Select Destination Folder", command=lambda: select_folder(destination_path))
select_destination_folder_button.pack()

# Create UI components for folder exclusion
exclude_folder_button = tk.Button(root, text="Exclude Folder", command=exclude_folder)
exclude_folder_button.pack()

excluded_folders_label = tk.Label(root, text="Excluded Folders:")
excluded_folders_label.pack()

excluded_folders_list = Listbox(root, width=50)
excluded_folders_list.pack()

# Create UI components for starting the sorting process
start_button = tk.Button(root, text="Start Sorting", command=start_sorting)
start_button.pack()

# Run the application
root.mainloop()
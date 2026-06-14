import shutil
import os


def clear_folder(folder_path: str) -> None:
    if os.path.isdir(folder_path): # Folder exists, delete it and re-create it
        shutil.rmtree(folder_path)
    os.mkdir(folder_path)

def copy_folder_content(source_folder: str, destination_folder: str) -> None: # Recursive function to copy the content of a folder
    if os.path.isdir(source_folder):
        for item in os.listdir(source_folder):
            item_path = os.path.join(source_folder, item)
            if os.path.isfile(item_path):
                print(f'Copying file "{item}" to "{destination_folder}"')
                shutil.copy(item_path, destination_folder)
            elif os.path.isdir(item_path): # Recursively copy the content of subfolder(s)
                print(f'Creating subfolder "{item}" to "{destination_folder}"')
                new_subfolder = os.path.join(destination_folder, item)
                os.mkdir(new_subfolder)
                copy_folder_content(item_path, new_subfolder)
            else:
                raise Exception("{item} is neither a file nor a folder (this error should not be raised)")
    else:
        raise FileNotFoundError(f"Folder {source_folder} does not exist")

def clear_then_copy(source_folder: str, destination_folder: str) -> None:
    clear_folder(destination_folder)
    copy_folder_content(source_folder, destination_folder)
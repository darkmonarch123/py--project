import os
import shutil

def organize_folder(target_folder):
    # 1. Dictionary mapping file extensions to folder names
    file_types = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
        'Documents': ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.pptx'],
        'Audio': ['.mp3', '.wav', '.aac'],
        'Videos': ['.mp4', '.mkv', '.avi'],
        'Archives': ['.zip', '.rar', '.7z'],
        'Programs': ['.exe', '.msi']
    }

    # 2. Change the current working directory to the target folder
    try:
        os.chdir(target_folder)
    except FileNotFoundError:
        print("Error: The specified folder does not exist.")
        return

    # 3. Scan all files in the folder
    files = [f for f in os.listdir() if os.path.isfile(f)]

    moved_count = 0

    for file in files:
        # Get the file extension (and convert to lowercase)
        filename, extension = os.path.splitext(file)
        extension = extension.lower()

        # Check which category this file belongs to
        category_found = False
        for folder_name, extensions in file_types.items():
            if extension in extensions:
                # Create the category folder if it doesn't exist
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                
                # Move the file into the new folder
                print(f"Moving: {file} -> {folder_name}/")
                shutil.move(file, folder_name)
                moved_count += 1
                category_found = True
                break
        
        # Optional: Put unknown file types into an "Others" folder
        if not category_found and extension != '':
            if not os.path.exists('Others'):
                os.makedirs('Others')
            print(f"Moving: {file} -> Others/")
            shutil.move(file, 'Others')
            moved_count += 1

    print(f"\nTask Complete! Successfully organized {moved_count} files.")

# --------------------------------------------------------
# Main Execution
# --------------------------------------------------------
if __name__ == "__main__":
    # Paste the path to your test folder here. 
    # (Use 'r' before the string to handle Windows backslashes correctly)
    target = r"C:\Users\salam\Downloads" 
    
    print(f"Starting organization in: {target}\n")
    organize_folder(target)
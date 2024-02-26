import os
import shutil
import configparser
import time
import matplotlib.pyplot as plt

CONFIG_FILE = 'config.ini'


def create_folder_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def move_files_to_folders(source_dir, destination_dir, excluded_files):
    start_time = time.time()
    files_moved_count = 0
    file_types_displaced = set()
    files_moved_histogram = {}

    for filename in os.listdir(source_dir):
        if filename != "Desktop Cleaner" and not filename.startswith("."):  # Exclude the script and hidden files
            file_path = os.path.join(source_dir, filename)
            if os.path.isfile(file_path) and file_path not in excluded_files:
                file_type = filename.split('.')[-1]  # Get file extension
                files_moved_histogram[file_type] = files_moved_histogram.get(file_type, 0) + 1

                target_dir = os.path.join(destination_dir, file_type)
                create_folder_if_not_exists(target_dir)
                shutil.move(file_path, os.path.join(target_dir, filename))

                files_moved_count += 1
            else:
                file_types_displaced.add(file_type)

    end_time = time.time()
    duration = end_time - start_time

    return files_moved_count, file_types_displaced, duration, files_moved_histogram


def get_desktop_and_excluded_paths():
    desktop_path = input("Enter the path of your desktop: ")
    excluded_files = []
    num_excluded_files = int(input("Enter the number of files you do not wish to move: "))
    for i in range(num_excluded_files):
        file_path = input(f"Enter the path of file {i + 1}: ")
        excluded_files.append(file_path)

    return desktop_path, excluded_files


def save_config(desktop_path, excluded_files):
    config = configparser.ConfigParser()
    config['Paths'] = {
        'DesktopPath': desktop_path,
        'ExcludedFiles': ','.join(excluded_files)
    }
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)


def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        desktop_path = config['Paths']['DesktopPath']
        excluded_files = config['Paths']['ExcludedFiles'].split(',')
        return desktop_path, excluded_files
    else:
        return None, None


def main():
    desktop_path, excluded_files = load_config()
    if desktop_path is None:
        desktop_path, excluded_files = get_desktop_and_excluded_paths()
        save_config(desktop_path, excluded_files)

    desktop_cleaner_path = os.path.join(desktop_path, "Desktop Cleaner")
    create_folder_if_not_exists(desktop_cleaner_path)

    print("Welcome to Desktop Cleaner!")

    while True:
        print("\nMenu:")
        print("2. Move files")
        print("3. Change desktop path and excluded files")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("This algorithm will clean up your computer desktop!\n When prompted, enter your desktop path and that of the files you wish to spare.\n "
                  "Once the program is done running, some information about the file will be ")

        elif choice == '2'
            files_moved_count, file_types_displaced, duration, files_moved_histogram = move_files_to_folders(
                desktop_path, desktop_cleaner_path, excluded_files)
            print(f"\nSummary:")
            print(f"Number of files moved: {files_moved_count}")
            print(f"File types displaced: {', '.join(file_types_displaced)}")
            print(f"Time taken to move files: {duration:.2f} seconds")

            # Plotting pie chart
            plt.figure(figsize=(8, 6))
            plt.pie(files_moved_histogram.values(), labels=files_moved_histogram.keys(), autopct='%1.1f%%')
            plt.title('File Types Moved')
            plt.show()

            # Plotting histogram
            plt.figure(figsize=(10, 6))
            plt.bar(files_moved_histogram.keys(), files_moved_histogram.values(), color='skyblue')
            plt.xlabel('File Type')
            plt.ylabel('Number of Files')
            plt.title('Histogram of File Types Moved')
            plt.xticks(rotation=45)
            plt.show()

        elif choice == '3':
            desktop_path, excluded_files = get_desktop_and_excluded_paths()
            save_config(desktop_path, excluded_files)

        elif choice == '4':
            print("Exiting program. See you next time!")
            break

        else:
            print("Please enter a valid option!")
            main()



if __name__ == "__main__":
    main()
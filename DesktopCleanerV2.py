import os
import shutil
import configparser
import time
import matplotlib.pyplot as plt
import sys
import numpy as np

CONFIG_FILE = 'config.ini'
HISTORY_FILE = 'history.txt'


class DesktopCleaner:
    def __init__(self):
        self.desktop_path = None
        self.excluded_files = []
        self.desktop_cleaner_path = None

    def create_folder_if_not_exists(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def move_files_to_folders(self, source_dir, destination_dir, excluded_files, custom_grouping=False, delete=False):
        start_time = time.time()
        files_moved_count = 0
        file_types_displaced = set()
        files_moved_histogram = {}

        for filename in os.listdir(source_dir):
            if filename != "Desktop Cleaner" and not filename.startswith("."):
                file_path = os.path.join(source_dir, filename)
                if os.path.isfile(file_path):
                    file_type = filename.split('.')[-1]
                    if filename not in excluded_files:
                        if custom_grouping:
                            if file_type in ('png', 'jpeg', 'gif', 'heif'):
                                target_dir = os.path.join(destination_dir, "Pictures")
                            elif file_type in ('doc', 'docx', 'pdf'):
                                target_dir = os.path.join(destination_dir, "Documents")
                            elif file_type in ('xlsx', 'xls'):
                                target_dir = os.path.join(destination_dir, "Spreadsheets")
                            else:
                                target_dir = os.path.join(destination_dir, "Miscellaneous")
                        else:
                            target_dir = os.path.join(destination_dir, file_type)

                        self.create_folder_if_not_exists(target_dir)
                        if delete:
                            os.remove(file_path)
                        else:
                            shutil.move(file_path, os.path.join(target_dir, filename))

                        files_moved_histogram[file_type] = files_moved_histogram.get(file_type, 0) + 1
                        files_moved_count += 1
                    else:
                        file_types_displaced.add(file_type)

        end_time = time.time()
        duration = end_time - start_time

        return files_moved_count, file_types_displaced, duration, files_moved_histogram

    def get_desktop_and_excluded_files(self):
        self.desktop_path = input("Enter the path of your desktop: ")
        self.excluded_files = []
        num_excluded_files = int(input("Enter the number of files you do not wish to move: "))
        for i in range(num_excluded_files):
            file_name = input(f"Enter the name of file {i + 1} + its extension (ex: Formula Table.docx): ")
            self.excluded_files.append(file_name)

    def save_config(self):
        config = configparser.ConfigParser()
        config['Paths'] = {
            'DesktopPath': self.desktop_path,
            'ExcludedFiles': ','.join(self.excluded_files)
        }
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)

    def load_config(self):
        config = configparser.ConfigParser()
        if os.path.exists(CONFIG_FILE):
            config.read(CONFIG_FILE)
            self.desktop_path = config['Paths']['DesktopPath']
            self.excluded_files = config['Paths']['ExcludedFiles'].split(',')
        else:
            self.get_desktop_and_excluded_files()
            self.save_config()

    def save_history(self, history):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')  # Capture real-time
        history_entry = f"{current_time}: {history.split(', Time taken')[0]}"  # Extracting without time taken
        with open(HISTORY_FILE, 'a') as history_file:
            history_file.write(history_entry + '\n')


    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as history_file:
                return history_file.read()
        else:
            return "No previous runs."

    def delete_history(self):
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
            print("History deleted.")
        else:
            print("No previous runs.")

    def main(self):
        self.load_config()

        self.desktop_cleaner_path = os.path.join(self.desktop_path, "Desktop Cleaner")
        self.create_folder_if_not_exists(self.desktop_cleaner_path)

        print("Welcome to Desktop Cleaner!")

        while True:
            print("\nMenu:")
            print("1. About")
            print("2. Move files")
            print("3. Delete files")
            print("4. Change desktop path and excluded files")
            print("5. Previous Runs")
            print("6. Delete History")
            print("7. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                print(
                    '''\n This algorithm will clean up your computer desktop!\n When prompted, enter the path you want the program to organize and name of the files you wish to spare.\n Once the program is done running, some information such as the "Time Taken" to move the item(s) and the type of file(s) moved will be displayed through summary graphs.\n More graph options are now available with  the new update.''')

            elif choice == '2':
                grouping_option = input(
                    "Choose grouping option:\n1. Separate Folders\n2. Custom Grouping\nEnter your choice: ")
                if grouping_option == '1':
                    files_moved_count, file_types_displaced, duration, files_moved_histogram = self.move_files_to_folders(
                        self.desktop_path, self.desktop_cleaner_path, self.excluded_files)
                elif grouping_option == '2':
                    files_moved_count, file_types_displaced, duration, files_moved_histogram = self.move_files_to_folders(
                        self.desktop_path, self.desktop_cleaner_path, self.excluded_files, custom_grouping=True)
                else:
                    print("Invalid option! Please choose 1 or 2.")
                    continue

                if files_moved_count == 0:
                    print("No files to be moved!")
                    break

                print(f"\nSummary:")
                print(f"Number of files moved: {files_moved_count}")
                print(f"File types displaced: {', '.join(file_types_displaced)}")
                print(f"Time taken to move files: {duration:.2f} seconds")

                # Ask the user if they want to see the graphs
                show_graphs = input("Do you want to see the summary of files displaced? (yes/no): ")
                if show_graphs.lower() == 'yes':
                    # Pie chart
                    plt.figure(figsize=(8, 6))
                    plt.pie(files_moved_histogram.values(), labels=files_moved_histogram.keys(), autopct='%1.1f%%')
                    plt.title('File Types Moved')
                    plt.show()

                    # Histogram
                    plt.figure(figsize=(10, 6))
                    plt.bar(files_moved_histogram.keys(), files_moved_histogram.values(), color='blue')
                    plt.xlabel('File Type')
                    plt.ylabel('Number of Files')
                    plt.title('Histogram of File Types Moved')
                    plt.xticks(rotation=45)
                    plt.show()

                    # NEW graphs
                    # Line graph
                    plt.figure(figsize=(10, 6))
                    plt.plot(list(files_moved_histogram.keys()), list(files_moved_histogram.values()), marker='o')
                    plt.xlabel('File Type')
                    plt.ylabel('Number of Files')
                    plt.title('Line Graph of File Types Moved')
                    plt.xticks(rotation=45)
                    plt.show()

                    # Scatter plot
                    plt.figure(figsize=(10, 6))
                    plt.scatter(list(files_moved_histogram.keys()), list(files_moved_histogram.values()))
                    plt.xlabel('File Type')
                    plt.ylabel('Number of Files')
                    plt.title('Scatter Plot of File Types Moved')
                    plt.xticks(rotation=45)
                    plt.show()

                    # Horizontal bar graph
                    plt.figure(figsize=(10, 6))
                    plt.barh(list(files_moved_histogram.keys()), list(files_moved_histogram.values()), color='green')
                    plt.xlabel('Number of Files')
                    plt.ylabel('File Type')
                    plt.title('Horizontal Bar Graph of File Types Moved')
                    plt.show()

                # Save history
                history = f"Files moved: {files_moved_count}, Time taken: {duration:.2f} seconds"
                self.save_history(history)

            elif choice == '3':
                confirm = input("Are you sure you want to delete files? (yes/no): ")
                if confirm.lower() == 'yes':
                    files_deleted_count, _, _, _ = self.move_files_to_folders(
                        self.desktop_path, self.desktop_cleaner_path, self.excluded_files, delete=True)
                    print(f"{files_deleted_count} files deleted.")
                else:
                    print("Operation cancelled.")

            elif choice == '4':
                self.get_desktop_and_excluded_files()
                self.save_config()

            elif choice == '5':
                print("\nPrevious Runs:")
                print(self.load_history())

            elif choice == '6':
                confirm = input("Are you sure you want to delete history? (yes/no): ")
                if confirm.lower() == 'yes':
                    self.delete_history()
                else:
                    print("Operation cancelled.")

            elif choice == '7':
                print("Exiting program. See you next time!")
                break

            else:
                print("Please enter a valid option!")


if sys.version_info < (3, 11):
    print("This program runs on Python 3.11 or later")
    sys.exit(1)

if __name__ == "__main__":
    cleaner = DesktopCleaner()
    cleaner.main()



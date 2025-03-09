import difPy
import argparse
import os

parser = argparse.ArgumentParser()

# Configure Arguments Passed to the Script
parser.add_argument("-s", "--single_directory", help="Search for duplicates in a single directory, options are true or false")
parser.add_argument("-d", "--multiple_directories", help="Search for duplicates in multiple directories, options are true or false")
parser.add_argument("-m", "--mode", help="Delete duplicates, options are delete or copy")

# Work with the Arguments Passed to the Script
args = parser.parse_args()

# Check that the user has specified a search option and take some input from the user.
if args.single_directory == "true":
    print("Searching for duplicates in a single directory")
    source_directory_path = input("Enter the path to the directory to search for duplicates: ")
elif args.multiple_directories == "true":
    print("Searching for duplicates in multiple directories")
    source_directory_paths = input("Enter multiple directory paths to search for duplicates, separated with commas: ")
    final_source_directory_paths = source_directory_paths.split(",")
elif args.single_directory == "false" and args.multiple_directories == "false":
    print("Please specify a search option")
    exit()
elif args.delete == "true" and args.copy == "true":
    print("Please specify only one deduplication mode")
    exit()

if args.mode == "delete":
    print("Deleting duplicates")
    do_delete = input("Are you sure that you want to continue? Y/N: ")
    if do_delete == "Y":
        deduplication_mode = "delete"
    else:
        exit()
elif args.mode == "copy":
    print("Copying duplicates into another directory")
    destination_folder = input("Enter the path to the destination directory: ")
    do_copy = input("Are you sure that you want to continue? Y/N: ")
    if do_copy == "Y":
        deduplication_mode = "copy"
    else:
        exit()
else:
    print("Please specify a deduplication mode")
    exit()

# Check that the source directory exists
if args.single_directory == "true":
    if not os.path.exists(source_directory_path):
        print("The source directory does not exist")
        exit()
elif args.multiple_directories == "true":
    for source_directory_path in final_source_directory_paths:
        if not os.path.exists(source_directory_path):
            print("The source directory does not exist")
            exit()

# Check that the destination directory exists, if we are copying duplicates.
if deduplication_mode == "copy":
    if not os.path.exists(destination_folder):
        print("The destination directory does not exist")
        exit()

# Find our duplicates.
if args.single_directory == "true":
    dif = difPy.build(source_directory_path)
    search = difPy.search(dif)
elif args.multiple_directories == "true":
    dif = difPy.build(source_directory_paths)
    search = difPy.search(dif)

# Do the deduplication
if deduplication_mode == "delete":
    search.delete(silent_del=False)
elif deduplication_mode == "copy":
    search.move_to(destination_path=destination_folder)
import difPy
import argparse
import os

parser = argparse.ArgumentParser()

# Configure Arguments Passed to the Script
parser.add_argument("-s", "--single_directory", help="Search for duplicates in a single directory, options are true or false")
parser.add_argument("-m", "--multiple_directories", help="Search for duplicates in multiple directories, options are true or false")
parser.add_argument("-d", "--delete", help="Delete duplicates, options are true or false")
parser.add_argument("-c", "--copy", help="Copy duplicates into another directory, options are true or false")
parser.add_argument("-f", "--destination_folder", help="Destination folder for copied duplicates, pass in if copy mode is selected")

# Work with the Arguments Passed to the Script
args = parser.parse_args()

if args.single_directory == "true" and args.multiple_direct == "false":
    print("Searching for duplicates in a single directory")
    source_directory_path = input("Enter the path to the directory to search for duplicates: ")
elif args.multiple_direct == "true" and args.single_directory == "false":
    print("Searching for duplicates in multiple directories")
    source_directory_paths = input("Enter multiple directory paths to search for duplicates, separated with commas: ")
    final_source_directory_paths = source_directory_paths.split(",")
else:
    print("Please specify a search option")
    exit()

if args.delete == "true":
    print("Deleting duplicates")
    deduplication_mode = "delete"
elif args.copy == "true":
    print("Copying duplicates into another directory")
    deduplication_mode = "copy"
else:
    print("Please specify a deduplication mode")
    exit()

# Check that the source directory exists
if args.single_directory == "true":
    if not os.path.exists(source_directory_path):
        print("The source directory does not exist")
        exit()
elif args.multiple_direct == "true":
    for source_directory_path in final_source_directory_paths:
        if not os.path.exists(source_directory_path):
            print("The source directory does not exist")
            exit()

# Check that the destination directory exists, if we are copying duplicates.
if deduplication_mode == "copy":
    if not os.path.exists(args.destination_folder):
        print("The destination directory does not exist")
        exit()

# Find our duplicates.
if args.single_directory == "true":
    dif = difPy.build(source_directory_path)
    search = difPy.search(dif)
elif args.multiple_direct == "true":
    dif = difPy.build(source_directory_paths)
    search = difPy.search(dif)

# Do the deduplication
if deduplication_mode == "delete":
    search.delete(silent_del=False)
elif deduplication_mode == "copy":
    search.move_to(destination_path=args.destination_folder)

import os
import zipfile

def get_file_size(file_path):
    """Returns the size of the file in bytes."""
    return os.path.getsize(file_path)

def create_zip_archive(zip_name, files):
    """Creates a zip archive with the given files."""
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))

def zip_files_in_directory(input_directory, output_directory, max_zip_size_mb=500):
    """Zips files in the input directory ensuring each zip is no larger than max_zip_size_mb, and stores them in the output directory."""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    files_to_zip = []
    current_zip_size = 0
    zip_counter = 1

    max_zip_size_bytes = max_zip_size_mb * 1024 * 1024

    for root, _, files in os.walk(input_directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = get_file_size(file_path)

            if current_zip_size + file_size > max_zip_size_bytes:
                # Create a new zip file since the current one exceeds the size limit
                zip_name = os.path.join(output_directory, f"archive_{zip_counter}.zip")
                create_zip_archive(zip_name, files_to_zip)
                print(f"Created {zip_name} with {len(files_to_zip)} files")

                # Reset for the next zip file
                zip_counter += 1
                files_to_zip = []
                current_zip_size = 0

            # Add the current file to the list and update the current zip size
            files_to_zip.append(file_path)
            current_zip_size += file_size

    # Create the last zip file if there are remaining files
    if files_to_zip:
        zip_name = os.path.join(output_directory, f"archive_{zip_counter}.zip")
        create_zip_archive(zip_name, files_to_zip)
        print(f"Created {zip_name} with {len(files_to_zip)} files")

# Directory containing AS400 program files
input_directory = 'path_to_your_as400_files_directory'
# Directory to save the zip files
output_directory = 'path_to_your_output_directory'

zip_files_in_directory(input_directory, output_directory)

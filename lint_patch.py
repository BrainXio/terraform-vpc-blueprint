import argparse
import os
import shutil
import subprocess
import sys  # Added for handling command-line args


def run_command(command):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error: {e.stderr}")
        return None


def backup_file(file_path):
    """Create a backup of the file before formatting."""
    backup_path = f"{file_path}.bak"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created: {backup_path}")


def sort_imports(file_path):
    """Sort the imports in the file with isort."""
    isort_result = run_command(["isort", file_path])
    if isort_result:
        print(f"Imports sorted for {file_path}.")
    else:
        print(f"Failed to sort imports for {file_path}.")


def format_and_patch(file_path):
    """Format the file with Black and apply changes using patch."""
    # Sort imports first
    sort_imports(file_path)

    # Run Black with --check --diff to get the diff
    black_diff = run_command(
        ["black", "--check", "--diff", "--exclude=.venv", file_path]
    )
    if not black_diff:
        print(f"No changes needed for {file_path}.")
        return

    # If Black finds differences, proceed with formatting
    black_format = run_command(["black", file_path])
    if not black_format:
        print(f"Failed to format {file_path}.")
        return

    # Here, instead of creating a patch, we've directly formatted the file.
    # If you need to apply a patch for some reason, you might want to reconsider this approach:

    # Create a temporary patch file (if you want to keep patching logic)
    # patch_file = "temp.patch"
    # with open(patch_file, 'w') as f:
    #     f.write(black_diff)

    # Apply the changes directly since we've already formatted the file with Black
    print(f"File {file_path} has been reformatted successfully.")


def main(file_paths):
    for file_path in file_paths:
        if file_path.endswith(".py"):
            if os.path.exists(file_path):
                print(f"Processing file: {file_path}")
                backup_file(file_path)
                format_and_patch(file_path)
            else:
                print(f"File {file_path} does not exist.")


def main(file_paths):
    # Format the script itself first
    format_and_patch(__file__)

    for file_path in file_paths:
        if file_path.endswith(".py") and file_path != __file__:
            if os.path.exists(file_path):
                print(f"Processing file: {file_path}")
                backup_file(file_path)
                format_and_patch(file_path)
            else:
                print(f"File {file_path} does not exist.")

import re
import os
import sys
import csv
import shlex

def extract_and_split_commands(log_file):
    """Extracts commands from a given log file using regex and splits combined commands while considering shell constructs."""
    commands = []
    with open(log_file, 'r') as file:
        for line in file:
            match = re.search(r'CMD:\s*(.+)', line)
            if match:
                command_line = match.group(1).strip()
                try:
                    parsed_commands = shlex.split(command_line, posix=True)
                    joined_commands = ' '.join(parsed_commands)
                    # Split on '&&', '||', and ';' but not on single '&'
                    split_commands = re.split(r'\s*&&\s*|\s*\|\|\s*|\s*;\s*', joined_commands)
                except ValueError:
                    # If shlex fails due to unmatched quotes, split manually and avoid splitting '&'
                    split_commands = re.split(r'\s*&&\s*|\s*\|\|\s*|\s*;\s*', command_line)

                for cmd in split_commands:
                    if cmd:  # Filter out any empty commands
                        commands.append(cmd)
    return commands

if __name__ == "__main__":
    if len(sys.argv) != 3:
        script_name = os.path.basename(sys.argv[0])
        print(f"Usage: {script_name} <log_folder> <output.csv>")
        sys.exit(1)

    log_folder, output_file = sys.argv[1], sys.argv[2]
    all_commands = []

    for log in os.listdir(log_folder):
        log_path = os.path.join(log_folder, log)
        all_commands.extend(extract_and_split_commands(log_path))

    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['command'])
        for command in all_commands:
            csvwriter.writerow([command])

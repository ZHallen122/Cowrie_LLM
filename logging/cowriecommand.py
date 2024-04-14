import re
import os
import sys
import csv
import base64

def extract_commands(data, log_file):
    with open(log_file, 'r') as f:
        for line in f:
            # match = re.search(r'^.* \[twisted.conch.ssh.session#info\] Executing command "(.*)"', line)
            match = re.search(r'CMD: \s*(.+)', line)
            if match:
                # command = match.groups()
                # data.append(command[0][2:-1])
                data.append(match.group(1).strip())

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: %s <logfolder> <output.csv>" % os.path.basename(sys.argv[0]))
        sys.exit(1)
    path = sys.argv[1]
    fields = ['command']

    logs = os.listdir(path)
    data = list()
    for log in logs:
        extract_commands(data, os.path.join(path, log))

    outFile = sys.argv[2]
    template = "{data},\n"
    with open(outFile, 'w') as file:
        for datum in data:
            fDatum = (str(datum))
            file.write(template.format(data = fDatum))

import re
import os
import sys
import csv

reconnections = 0
ip_commands = dict()
ip_connections = set()
current_ip = ""
avgConTime = 0

def extract_commands(log_file):
    global ip_commands
    global reconnections
    global ip_connections
    global file_data
    ip_commands = dict()
    ip_connections = set()
    ip_reconnection = set()

    reconnections = 0
    unique_reconnects = 0
    with open(log_file, 'r') as f:
        for line in f:
            command_match = re.match(r'^.* \[HoneyPotSSHTransport,\d+,([\d\.]*)\] (.*)', line)
            if command_match:
                ip, command = command_match.groups()
                if ip not in ip_commands:
                    ip_commands[ip] = []
                ip_commands[ip].append(command)
            entry_match = re.match(r'^.* \[cowrie.ssh.factory.CowrieSSHFactory\] New connection: ([\d\.]*):\d\d\d\d\d', line)
            if entry_match:
                connect_ip = entry_match.groups()
                if connect_ip not in ip_connections:
                    ip_connections.add(connect_ip)
                else:
                    reconnections+=1
                    if connect_ip not in ip_reconnection:
                        ip_reconnection.add(connect_ip)
                        unique_reconnects+=1
            

        file_data['reconnections'] = reconnections
        file_data['unique reconnections'] = unique_reconnects

def extract_avg(ip_commands):
    global file_data
    totalConTime = 0
    conCount = 0
    conTimeRegex = re.compile("Connection lost after ([0-9]+) seconds\s*")
    firstNumRegex = re.compile(r'\d+')
    for ip, commands in ip_commands.items():
        for command in commands:
            if conTimeRegex.match(command) is not None:
                totalConTime += int(firstNumRegex.search(commands[-1]).group())
                conCount+=1
    avgConTime = totalConTime/conCount
    file_data['avg connection time'] = avgConTime

if __name__ == "__main__":
    global file_data
    if len(sys.argv) != 3:
        print("Usage: %s <logfolder> <output.csv>" % os.path.basename(sys.argv[0]))
        sys.exit(1)

    path = sys.argv[1]
    logs = os.listdir(path)
    date = "{m}/{d}/{y}"
    data = list()
    for log in logs:
        year = re.search(".*\.(\d\d\d\d)-\d\d-\d\d", log)
        month = re.search(".*\.\d\d\d\d-(\d\d)-\d\d", log)
        day = re.search(".*\.\d\d\d\d-\d\d-(\d\d)", log)
        logDate = date.format(m = month.groups(0)[0], d = day.groups(0)[0], y = year.groups(0)[0])

        file_data = dict()
        file_data['date'] = logDate
        extract_commands(os.path.join(path, log))
        extract_avg(ip_commands)
        data.append(file_data)

    outFile = sys.argv[2]
    with open(outFile, 'w') as csvfile:
        fields = ['date', 'avg connection time', 'reconnections', 'unique reconnections']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

#! /usr/share/python3 

import requests
import socket
import subprocess
import json
import datetime
import optparse

master_ip = '192.168.242.93'
bot_name = "america"
bot_ip = "192.168.242.93"

def get_arguements():

    parser = optparse.OptionParser()
    parser.add_option("-n", "--bot_name", help="Name for the bot", dest="bot_name")
    parser.add_option("-m", "--master_ip", help="IP Address of the master server", dest="master_ip")
    parser.add_option("-b", "--bot_ip", help="IP Address of the bot server", dest="bot_ip")

    (options, arguements) = parser.parse_args()

    if not options.bot_name:
        parser.error("[-] Please specify the bot IP Name, use --help for more information")
    if not options.master_ip:
        parser.error("[-] Please specify the Master IP address, use --help for more information")
    if not options.bot_ip:
        parser.error("[-] Please specify the bot IP Address, use --help for more information")
    else:
        return options

def log_output(data):
    with open(log_file, 'a') as file:
        file.write(data)

def initiate(master_ip, bot_name, bot_ip):
    print("[*] Registering bot to the API Server .... ")
    request = requests.get('http://127.0.0.1:5000/bot_register?bot_name=' + bot_name + '&bot_ip=' + bot_ip)
    if request.text == "200 OK":
        print("[+] Bot has been registered to the master server!\n")
    else:
        print("[-] Failed to register the Bot to the master server!")
        exit()

def data_collecter():
    data_sheet = [bot_name, bot_ip]
    command = ['osqueryi', '--json', 'command']
    queries = ['select * from cpu_time;']
    for query in queries:
        command[2] = query
        result = subprocess.run(command, capture_output=True, text=True)
        response = json.loads(result.stdout)
        data_sheet.append(response)

    return data_sheet

def communicate_to_master(master_ip):
    json_data = json.dumps(data_collecter())
    log_output(json_data + '\n\n')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((master_ip, 4444))
        sock.sendall(bytes(json_data,encoding="utf-8"))

    finally:
        sock.close()

log_file = bot_name + "_history.log"
initiate(master_ip, bot_name, bot_ip)

try:
    while True:
        listner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        
        listner.bind((bot_ip, 5555))                                     
        listner.listen(0)   
        print("[+] Ready to accept connection from master .... ")                                                 
        connection, address = listner.accept()                        
        recieved_data = connection.recv(1024)
        if recieved_data.decode() == "data request":
            print("[*] Data request recieved, communication with master initiated at: " + str(datetime.datetime.now()))
            log_output("Data request recieved from master server at: " + str(datetime.datetime.now()) + '\n')
            communicate_to_master(master_ip)
            print("[+] Communication with master successful!\n")

except KeyboardInterrupt:
    result = requests.get('http://127.0.0.1:5000/bot_disconnect?bot_name=' + bot_name)
    if result.text == "200 OK":
        print("[+] Bot has been sucessfully disconnected and shut down.")
    else:
        print("[-] Failed to disconnect with master server and proper shut-down.")
    log_output("Bot was shut-down at: " + str(datetime.datetime.now()) + '\n')
    exit()
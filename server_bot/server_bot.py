#! /usr/share/python3 

import requests
import socket
import subprocess
import json

master_ip = '192.168.242.93'
bot_name = "aditya"
bot_ip = "192.168.242.93"

def initiate(master_ip, bot_name, bot_ip):
    print("[*] Registering bot to the API Server .... ")
    request = requests.get('http://127.0.0.1:5000/register_bot?bot_name=' + bot_name + '&bot_ip=' + bot_ip)
    if request.text == "200 OK":
        print("[+] Bot has been registered to the master server!")
    else:
        print("[-] Failed to register the Bot to the master server!")
        exit()

def data_collecter():
    data_sheet = []
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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((master_ip, 4444))
        sock.sendall(bytes(json_data,encoding="utf-8"))

    finally:
        sock.close()

initiate(master_ip, bot_name, bot_ip)

while True:
    listner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        
    listner.bind((bot_ip, 5555))                                     
    listner.listen(0)   
    print("[+] Ready to accept connection from master .... ")                                                 
    connection, address = listner.accept()                        
    recieved_data = connection.recv(1024)
    if recieved_data.decode() == "data request":
        print("[*] Data request recieved, communication with master initiated.")
        communicate_to_master(master_ip)
        print("[+] Communication with master successful!")
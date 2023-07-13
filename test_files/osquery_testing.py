# /usr/share/python3 

import subprocess
import json
import socket

# command = ['osqueryi', '--json', 'select * from users']

# result = subprocess.run(command, capture_output=True, text=True)

# if result.returncode == 0:
#     response = json.loads(result.stdout)
#     for i in response:
#         key = i.keys()
#         for t in key:
#             print(str(t) + " = " + str(i[t]))
#         print("--------------------------")

while True:
    listner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        
    listner.bind(('192.168.242.93', 4444))                                     
    listner.listen(0)                                                    
    #print("[+] Waiting for incomming connections .... ")
    connection, address = listner.accept()                          
                                                                             
    #print("[+] Connection recieved from " + str(address))

    recieved_data = connection.recv(1024 * 100)
    print(recieved_data.decode())

# def data_collecter():
#     data_sheet = []
#     command = ['osqueryi', '--json', 'command']
#     queries = ['select * from users;', 'select * from cpu_time;']
#     for query in queries:
#         command[2] = query
#         result = subprocess.run(command, capture_output=True, text=True)
#         response = json.loads(result.stdout)
#         data_sheet.append(response)

#     return data_sheet[]

# print(data_collecter())
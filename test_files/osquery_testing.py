# /usr/share/python3 

import subprocess
import json

command = ['osqueryi', '--json', 'select * from users']

result = subprocess.run(command, capture_output=True, text=True)

if result.returncode == 0:
    response = json.loads(result.stdout)
    for i in response:
        key = i.keys()
        for t in key:
            print(str(t) + " = " + str(i[t]))
        print("--------------------------")
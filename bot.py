"""
adventure-bot

This bot listens incoming connections from Facebook.

Any message is sent as potential Javascript to node, and the console output
is sent back as a response.

"""

from flask import Flask, request
from pymessenger.bot import Bot

from server import Server

import os

app = Flask(__name__)
bot = Bot(os.environ['token'])
gameserver = Server(os.path.join(os.dirname(os.abspath(__file__)),
                                 'scottadams', 'assets', os.environ['datafile']))


@app.route("/webhook", methods=['GET', 'POST'])
def server():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == os.environ['challenge']:
                return request.args.get("hub.challenge")

    if request.method == 'POST':
        output = request.json
        event = output['entry'][0]['messaging']
        for x in event:
            if (x.get('message') and x['message'].get('text')):
                command = x['message']['text']
                recipient_id = x['sender']['id']

                message = gameserver.play(recipient_id, command)
                bot.send_text_message(recipient_id, message)

                return message
            else:
                pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

"""
adventure-bot

This bot listens incoming connections from Facebook.

Any message is sent as potential Javascript to node, and the console output
is sent back as a response.

"""

from server import Server

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from pymessenger.bot import Bot

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

bot = Bot(os.environ['token'])
gameserver = Server(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'scottadams', 'assets', os.environ['datafile']), db, app.logger)


@app.route("/webhook", methods=['GET', 'POST'])
def server():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == os.environ['challenge']:
                return request.args.get("hub.challenge")

    if request.method == 'POST':
        output = request.json
        event = output['entry'][0]['messaging']
        for x in event:
            if x.get('message') and x['message'].get('is_echo'):
                app.logger.info('Skipping echo')
                return 'ok'

            if (x.get('message') and x['message'].get('text')):
                command = x['message']['text']
                recipient_id = x['sender']['id']

                message = gameserver.play(recipient_id, command)
                bot.send_text_message(recipient_id, message)

                app.logger.info('Handled request: %s', request.json)

                return message
            else:
                pass

    app.logger.info('Unknown request: %s', request.json)

    return 'ok'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

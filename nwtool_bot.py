import logging
import os
import socketserver
from datetime import datetime
from subprocess import Popen, STDOUT, PIPE

from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater

from web import SimpleHTTPRequestHandler


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Your network tools in telegram. Use specific commands to execute some tools.")


def text_to_args(text):
    args = text.split()
    args[0] = args[0][1:]
    print("request: ", args)
    return args


def dig(update, context):
    args = text_to_args(update.message.text)
    process = Popen(args, stdout=PIPE, stderr=STDOUT)
    response = process.stdout.read().decode('utf-8')
    send_response(response, update, context)


def whois(update, context):
    args = text_to_args(update.message.text)
    process = Popen(args, stdout=PIPE, stderr=STDOUT)
    response = process.stdout.read().decode("utf-8")
    print("response: ", response)
    send_response(response, update, context)


def host(update, context):
    args = text_to_args(update.message.text)
    process = Popen(args, stdout=PIPE, stderr=STDOUT)
    response = process.stdout.read().decode("utf-8")
    print("response: ", response)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    send_response(response, update, context)


def echo(update, context):
    send_response('Unknown command. Try some of known command...', update, context)


def send_response(response, update, context):
    chunk_size = 4096
    for i in range(0, len(response), chunk_size):
        context.bot.send_message(chat_id=update.effective_chat.id, text=response[i:i + chunk_size])


token = os.environ['TG_TOKEN']
PORT = int(os.environ['PORT'])
startedAt = datetime.now()

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

dispatcher.add_handler(CommandHandler('start', start))
# dispatcher.add_handler(MessageHandler(Filters.text('dig .*'), dig))
dispatcher.add_handler(CommandHandler('dig', dig))
dispatcher.add_handler(CommandHandler('host', host))
dispatcher.add_handler(CommandHandler('whois', whois))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

updater.start_polling()

with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.RequestHandlerClass.startedAt = startedAt
    httpd.serve_forever()

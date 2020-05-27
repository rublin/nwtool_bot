import logging
import socketserver
import sys
from http.server import BaseHTTPRequestHandler
from subprocess import check_output, Popen, STDOUT, PIPE

from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater


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
    result = check_output(args).decode('utf-8')
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)


def host(update, context):
    args = text_to_args(update.message.text)
    process = Popen(args, stdout=PIPE, stderr=STDOUT)
    response = process.stdout.read().decode("utf-8")
    print("response: ", response)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Unknown command. Try some of known command...')


if len(sys.argv) < 2:
    print("Pass the token as a first argument")
    print("python nwtool_bot.py <TOKEN>")
    sys.exit(2)

updater = Updater(token=sys.argv[1], use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

dispatcher.add_handler(CommandHandler('start', start))
# dispatcher.add_handler(MessageHandler(Filters.text('dig .*'), dig))
dispatcher.add_handler(CommandHandler('dig', dig))
dispatcher.add_handler(CommandHandler('host', host))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

updater.start_polling()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')


PORT = 8080

with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()

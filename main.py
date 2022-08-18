from flask import Flask, Response, request
import requests
import telegram
import telebot
from sympy import isprime
import math

TOKEN = '5553907786:AAGxSrvF8dXHEqV4oS9nOSdP5IivlOxfZH0'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://4984-82-80-173-170.eu.ngrok.io/message'.format(TOKEN)

app = Flask(__name__)

list_commands = ['prime', 'factorial', 'palindrome', 'sqrt']
char = '/'


def print_connect() -> str:
    string = "Hey you,\nWelcome to Group-13-bot!\n\nIt's your options:\n"
    for i, command in enumerate(list_commands):
        string += f'{i+1}. /{command} (your number).\n'
    return string


def return_and_stop(chat_id, result: str):
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                       .format(TOKEN, chat_id, result))
    return Response("success")


def check_prime(number_bot: int) -> str:
    if number_bot != 2 and number_bot % 2 == 0:
        return "Come on dude, you know even numbers are not prime!"
    elif isprime(number_bot):
        return "I'm prime! :)"
    else:
        return "I'm not prime! :("


def isFactorial(number_bot: int) -> str:
    factorial = 1
    count = 1
    while factorial <= number_bot:
        if factorial == number_bot:
            return f'I result of factorial operation ({count})!'
        count = count + 1
        factorial = factorial * count
    return "I not result of factorial operation!"


def isPalindrome(number_bot: int) -> str:
    if str(number_bot) == str(number_bot)[::-1]:
        return "I'm palindrome! :)"
    return "I'm not palindrome! :("


def isSqrt(number_bot: int) -> str:
    sqrt_number = math.sqrt(number_bot)
    if sqrt_number % 1 == 0:
        return f'I have an integer square root ({sqrt_number})!'
    return f'I have not an integer square root ({sqrt_number})!'


@app.route('/message', methods=["POST"])
def handle_message():
    chat_id = request.get_json()['message']['chat']['id']

    input_command = str(request.get_json()['message']['text'])
    type_command = ""
    number_bot = ""
    result = ""

    try:
        type_command = input_command.split(' ')[0]
        number_bot = input_command.split(' ')[1]
    except:
        result = print_connect()
        return return_and_stop(chat_id, result)

    else:
        if number_bot.isdigit() is False:
            result = "The input is't number"
            return return_and_stop(chat_id, result)

        number_bot = int(number_bot)
        if type_command == char+list_commands[0]:
            result = check_prime(number_bot)
            return return_and_stop(chat_id, result)

        elif type_command == char+list_commands[1]:
            result = isFactorial(number_bot)
            return return_and_stop(chat_id, result)

        elif type_command == char+list_commands[2]:
            result = isPalindrome(number_bot)
            return return_and_stop(chat_id, result)

        elif type_command == char+list_commands[3]:
            result = isSqrt(number_bot)
            return return_and_stop(chat_id, result)

        else:
            return print_connect()


@app.route('/sanity')
def sanity():return "Server is running"


if __name__ == '__main__':
    requests.get(TELEGRAM_INIT_WEBHOOK_URL)
    app.run(port=5002)






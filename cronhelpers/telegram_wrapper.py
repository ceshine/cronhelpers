"""A decorator that sends the result of a function run to Telegram.

Adapted from https://github.com/huggingface/knockknock/blob/master/knockknock/telegram_sender.py
"""
import os
import datetime
import traceback
import functools
import socket
from typing import Optional

import telegram

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def telegram_wrapper(
        token: str, chat_id: int, name: Optional[str] = None,
        send_at_start: bool = False, send_on_success: bool = False):
    """Telegram sender wrapper: execute func, send a Telegram message with the end status
    (sucessfully finished or crashed) at the end. Also send a Telegram message before
    executing func.

    Parameters
    ----------
    token : str
        The API access TOKEN required to use the Telegram API.
        Visit https://core.telegram.org/bots#6-botfather to obtain your TOKEN.
    chat_id : int
        Your chat room id with your notification BOT.
        Visit https://api.telegram.org/bot<YourBOTToken>/getUpdates to get your chat_id
        (start a conversation with your bot by sending a message and get the `int` under
        message['chat']['id'])
    name : Optional[str], optional
        The name of this cron job. Leave it to None and the name of the function will be
        used.
    send_at_start : bool, optional
        Whether to send a message when the job is started.
    send_on_success : bool, optional
        Whether to send a message when the job is finished successfully.
    """

    bot = telegram.Bot(token=token)

    def decorator_sender(func):
        @functools.wraps(func)
        def wrapper_sender(*args, **kwargs):

            start_time = datetime.datetime.now()
            host_name = socket.gethostname()
            func_name = name
            if func_name is None:
                func_name = func.__name__

            if send_at_start:
                contents = ['%s has started 🎬' % func_name,
                            'Machine name: %s' % host_name]
                text = '\n'.join(contents)
                bot.send_message(chat_id=chat_id, text=text)
            try:
                value = func(*args, **kwargs)
                end_time = datetime.datetime.now()
                elapsed_time = end_time - start_time
                if send_on_success:
                    contents = ["%s has completed 🎉" % func_name,
                                'Machine name: %s' % host_name,
                                'Starting date: %s' % start_time.strftime(
                                    DATE_FORMAT),
                                'Execution duration: %s' % str(elapsed_time)]
                    try:
                        str_value = str(value)
                        contents.append(
                            'Main call returned value: %s' % str_value)
                    except:
                        contents.append('Main call returned value: %s' %
                                        "ERROR - Couldn't str the returned value.")
                    text = '\n'.join(contents)[:2000]
                    bot.send_message(chat_id=chat_id, text=text)
                return value

            except Exception as ex:
                end_time = datetime.datetime.now()
                elapsed_time = end_time - start_time
                contents = ["%s has crashed ☠️" % func_name,
                            'Machine name: %s' % host_name,
                            'Starting date: %s' % start_time.strftime(
                                DATE_FORMAT),
                            'Crash date: %s' % end_time.strftime(DATE_FORMAT),
                            'Crashed execution duration: %s\n\n' % str(
                                elapsed_time),
                            "Here's the error:",
                            '%s\n\n' % ex,
                            "Traceback:",
                            '%s' % traceback.format_exc()]
                text = '\n'.join(contents)
                bot.send_message(chat_id=chat_id, text=text)
                raise ex

        return wrapper_sender

    return decorator_sender

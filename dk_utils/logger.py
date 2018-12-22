# Functions to facilitate logs
# Author: D.Kisler <admin@dkisler.de>

import sys
import logging
import requests
import inspect


def lineno():
    """Returns the current line number in our program."""

    return inspect.currentframe().f_back.f_lineno


def slack_webhook(url, msg):
    """
    Function to send an error msg as a slack webhook

    :param url: string - slack webhook URL
    :param msg: string - the message text
    """

    try:
        res = requests.post(url, json={'text': 'Trk Processor',
                                       'attachments': [{'title': 'Error!',
                                                        'text': msg,
                                                        'color': '#FC1414'
                                                        }]
                                       })
    except:
        return False
    return res.ok


class Logger:

    """
    Logging class

    :param logfile: string - path where to write log into
    :param webhook_url: string - URL for webhook
    :param kill: boolean - shall the script be interrupted
    """

    def __init__(self, logfile, webhook_url=None, kill=True):

        self.url = webhook_url
        self.kill = kill

        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=logfile,
                            filemode='a+')
        self.logger = logging.getLogger('logs')

    def send(self, msg, linenum, info=False, send_webhook=True, kill=True, state=1):
        """
        Function to send the message to a log file, and to a webhook

        :param type: string - log message type error, or info
        :param msg: string - message to log
        :param info: boolean - is info message?
        :param send_webhook: boolen - shall the message be sent to webhook?
        :param kill: boolean - shall the script be interrupted
        :param state: [1,0] - error interruption state
        """

        if info:
            self.logger.info(f'{msg}. line: {linenum}.')
        else:
            self.logger.error(f'{msg}. line: {linenum}.')

        # send sebhook
        if self.url and send_webhook:
            _ = slack_webhook(self.url, f'Line: {linenum}\nError: {msg}')
        # kill the process
        if self.kill and kill:
            sys.exit(state)

# Functions to facilitate logs
# Author: D.Kisler <admin@dkisler.de>

import sys
import logging
import requests
import inspect


def lineno():
    """Returns the current line number in our program."""

    return inspect.currentframe().f_back.f_lineno

class Logger:

    """
    Logging class

    :param logfile: string - path where to write log into
    :param webhook: dict with webhook URL for and the webhook body:
                    e.g. {
                            'url':'webhook_url',
                            'body': {'text':'text of message',
                                      'msg':'attachment message here',
                                      'title':'attachment title here',
                                      'color':'attachment border color'
                                      }
                         }
    :param kill: boolean - shall the script be interrupted
    """

    def __init__(self, logfile, webhook=None, kill=True):

        self.webhook = webhook
        self.kill = kill

        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=logfile,
                            filemode='a+')
        self.logger = logging.getLogger('logs')

    @classmethod
    def send_slack(self, webhook):
        """
        Function to send an error msg as a slack webhook

        :param webhook: dict with webhook URL for and the webhook body:
                        e.g. {
                                'url':'webhook_url',
                                'body': {'text':'text of message',
                                          'msg':'attachment message here',
                                          'title':'attachment title here',
                                          'color':'attachment border color'
                                          }
                             }
        """

        try:
            res = requests.post(webhook['url'],
                                json={'text': webhook['body']['text'],
                                      'attachments': [{
                                          'title': webhook['body']['title'],
                                          'text': webhook['body']['msg'],
                                          'color': webhook['body']['color']}]
                                      })
        except Exception as ex:
            return False
        return True

    def send(self, msg, linenum=None, info=False, send_webhook=True, webhook=None, kill=True, state=1):
        """
        Function to send the message to a log file, and to a webhook

        :param type: string - log message type error, or info
        :param msg: string - message to log
        :param info: boolean - is info message?
        :param send_webhook: boolen - shall the message be sent to webhook?
        :param webhook: dict - webhook object
        :param kill: boolean - shall the script be interrupted
        :param state: [1,0] - error interruption state
        """
        if linenum:
            msg_send = f'{msg}.\nLine: {linenum}.'
        if not linenum or info:
            msg_send = f'{msg}.'

        if info:
            self.logger.info(msg_send)
        else:
            self.logger.error(msg_send)

        # send sebhook
        if send_webhook and (self.webhook or webhook):
            if webhook:
                webhk = webhook
            else:
                webhk = self.webhook

            webhk['body']['msg'] = msg_send

            _ = self.send_slack(webhk)
        # kill the process
        if self.kill and kill:
            sys.exit(state)

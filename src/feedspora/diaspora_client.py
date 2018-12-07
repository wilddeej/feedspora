"""
Diaspora client.
"""
import logging

import diaspy.connection
import diaspy.models
import diaspy.streams

from feedspora.generic_client import GenericClient


class DiaspyClient(GenericClient):
    ''' The DiaspyClient handles the connection to Diaspora. '''
    stream = None
    connection = None

    def __init__(self, account, testing):
        '''
        Initialize
        :param account:
        :param testing:
        '''

        if not testing:
            self.connection = diaspy.connection.Connection(
                pod=account['pod'],
                username=account['username'],
                password=account['password'])
            self.connection.login()
            try:
                self.stream = diaspy.streams.Stream(self.connection,
                                                    'stream.json')
            except diaspy.errors.PostError as exception:
                logging.error("Cannot get diaspy stream: %s", str(exception))
                self.stream = None
        self.keywords = []
        try:
            self.keywords = [
                word.strip() for word in account['keywords'].split(',')
            ]
        except KeyError:
            pass

    def post(self, entry):
        '''
        Post entry to Diaspora.
        :param entry:
        '''

        text = '['+entry.title+']('+entry.link+')' \
            + ' | ' + ''.join([" #{}".format(k) for k in self.keywords]) \
            + ' ' + ''.join([" #{}".format(k) for k in entry.keywords])
        to_return = True

        if self.stream:
            # pylint: disable=unexpected-keyword-arg
            to_return = self.stream.post(
                text, aspect_ids='public', provider_display_name='FeedSpora')
            # pylint: enable=unexpected-keyword-arg
        elif self.is_testing():
            to_return = self.test_output(text=text)
        else:
            logging.info("Diaspy stream is None, not posting anything")

        return to_return

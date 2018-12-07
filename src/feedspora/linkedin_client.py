"""
LinkedIn client
"""

from linkedin import linkedin

from feedspora.generic_client import GenericClient


class LinkedInClient(GenericClient):
    ''' The LinkedInClient handles the connection to LinkedIn. '''
    _linkedin = None
    _visibility = None

    def __init__(self, account, testing):
        '''
        Initialize
        :param account:
        :param testing:
        '''

        if not testing:
            self._linkedin = linkedin.LinkedInApplication(
                token=account['authentication_token'])
        self._visibility = account['visibility']

    def test_output(self, **kwargs):
        '''
        Print output for testing purposes
        :param kwargs:
        '''
        output = '>>> ' + self.get_name() + ' posting:\n' + \
            'Title: ' + self._trim_string(kwargs['entry'].title, 200)+'\n' + \
            'Link: ' + kwargs['entry'].link + '\n' + \
            'Visibility: ' + self._visibility+'\n' + \
            'Description: ' + self._trim_string(kwargs['entry'].title, 256) + \
            '\n' + \
            'Comment: ' + self._mkrichtext(kwargs['entry'].title,
                                           kwargs['entry'].keywords,
                                           maxlen=700)

        return self.output_test(output)

    def post(self, entry):
        '''
        Post entry to LinkedIn
        :param entry:
        '''
        to_return = False

        if self.is_testing():
            to_return = self.test_output(entry=entry)
        else:
            to_return = self._linkedin.submit_share(
                comment=self._mkrichtext(
                    entry.title, entry.keywords, maxlen=700),
                title=self._trim_string(entry.title, 200),
                description=self._trim_string(entry.title, 256),
                submitted_url=entry.link,
                visibility_code=self._visibility)

        return to_return

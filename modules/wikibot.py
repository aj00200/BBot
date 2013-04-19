'''Provide URLs for [[wikitext]] links.'''
import re
import api


class Module(api.Module):
    '''
    Send SSL Wikipedia links to a channel when someone puts the "link"
    brackets around some words.
    '''
    wiki_url = 'https://en.wikipedia.org/wiki/%s'
    def privmsg(self, nick, data, channel):
        data = api.get_message(data)
        if re.search('\[\[.*\]\]', data):
            word = data[data.find('[[') + 2:data.find(']]')]
            self.msg(channel, self.wiki_url % word)
